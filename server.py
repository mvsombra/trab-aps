from flask import Flask, request, g, session, redirect, url_for
from sessions import RedisSessionInterface
from desenha_tela import DesenhaTela as dt
from bd import AcessoBD
import os
import requests
import pickle

dba = AcessoBD()
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.session_interface = RedisSessionInterface()
draw = dt()


@app.route('/')
def index():
    p = dba.select_produtos(ultimos=6)
    sug = dba.produtos_mais_vendidos()
    return draw.render('index', p, sug)

@app.route('/compra', methods=['POST'])
def compra():
    i = 1
    while(True):
        if(request.form[str(i)]):
            print(request.form[str(i)])
            dba.insert_compra(request.form[str(i)], session['user'])
        else:
            break
        i += 1
    
    dba.esvaziar_carrinho(session['user'])
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if(not g.user):
        return redirect(url_for('index'))
    
    if(g.user[7] == 0):
        return redirect(url_for('index'))
    if("q" not in request.args):
        return redirect(url_for('index'))
    
    q = request.args["q"]
    if(q == "item"):
        produtos = dba.produtos_mais_vendidos(item=False)
        return draw.render('dashboard', produtos)
    elif(q == "valor"):
        produtos = dba.produtos_mais_vendidos()
        return draw.render('dashboard', produtos)
    else:
        return redirect(url_for('index'))


@app.route('/produtos')
def produtos():
    catlist = ["tapiocas", "bebidas"]
    if("cat" not in request.args):
        p = dba.select_produtos()
        sug = dba.produtos_mais_vendidos()
    else:
        if(request.args["cat"] in catlist):
            cat = catlist.index(request.args["cat"])
        else:
            cat = None
        p = dba.select_produtos(cat=cat)
        sug = dba.produtos_mais_vendidos(cat=cat)
    return draw.render('produtos', p, sug)


@app.route('/produto/', defaults={'cod': None})
@app.route('/produto/<cod>')
def ver_produto(cod):
    if(not cod):
        return redirect(url_for('index'))

    try:
        prod = dba.select_produtos(cod=cod)[0]
    except IndexError:
        return redirect(url_for('index'))

    return draw.render('ver-produto', prod)


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if(request.method == 'POST'):
        dba.insert_carrinho(session['user'], request.form['prod'])

    return draw.render('carrinho', dba.select_carrinho(session['user']))


@app.route('/excluir-carrinho', methods=['POST'])
def excluir_carrinho():
    dba.delete_carrinho(session['user'], request.form['prod'])
    return redirect(url_for('carrinho'))


@app.route('/notificacao', methods=['POST'])
def notificacao():
    dba.insert_notificacao(request.form['prod'], session['user'])
    return redirect(url_for('index'))


@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if(g.user):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        session.pop('user', None)
        if(dba.auth_user(request.form['email'], request.form['senha'])):
            session.permanent = True
            session['user'] = request.form['email']
            return redirect(url_for('index'))
        else:
            return draw.render('login')
    else:
        return draw.render('login')


@app.route('/sair')
def sair():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/add-produto', methods=['GET', 'POST'])
def add_produto():
    if(not g.user):
        return redirect(url_for('index'))

    if(g.user[7] == 0):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        dba.insert_produto(request.form['cod'], request.form['nome'],
                           request.form['preco'], bool(request.form['disp']),
                           request.form['tipo'], request.form['descricao'])
        return redirect(url_for('index'))

    return draw.render('addproduto')


@app.route('/edit-produto/', defaults={'prod': None})
@app.route('/edit-produto/<prod>', methods=['GET', 'POST'])
def edit_produto(prod):
    if(not g.user or not prod):
        return redirect(url_for('index'))

    if(g.user[7] == 0):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        disp = bool(int(request.form['disp']))
        dba.update_produto(request.form['cod'], request.form['nome'],
                           request.form['preco'], disp, request.form['tipo'],
                           request.form['descricao'])
        return redirect(url_for('index'))

    produto = dba.select_produtos(cod=prod)
    return draw.render('editproduto', produto)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if(g.user):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        session.pop('user', None)
        if(len(dba.select_users(email=request.form['email'])) == 0):
            if(request.form['senha'] == request.form['senha2']):
                dba.insert_user(request.form['nome'], request.form['cpf'],
                                request.form['data_nasc'],
                                request.form['telefone'],
                                request.form['endereco'],
                                request.form['email'], request.form['senha'])

                session.permanent = True
                session['user'] = request.form['email']
                return redirect(url_for('index'))
            else:
                return draw.render('cadastro')
        else:
            return draw.render('cadastro')
    else:
        pass
    return draw.render('cadastro')


@app.before_request
def before_request():
    emails = dba.select_notificacao()
    notificar_usuarios(emails)
    dba.delete_notificacao()
    g.user = None
    if('user' in session):
        g.user = dba.select_users(email=session['user'], max_results=1)


def notificar_usuarios(emails):
    credentials = pickle.load(open('mailgun.pkl', 'rb'))
    MAILGUN_DOMAIN_NAME = credentials['nome']
    MAILGUN_API_KEY = credentials['key']
    corpo = 'O produto que você esperava chegou na nossa loja!'
    corpo += ' Venha conferir!\n'
    corpo += 'https://tapiocadobilly.herokuapp.com'
    destino = []

    for cliente in emails:
        destino.append(cliente[0])

    if(len(destino) > 0):
        url = 'https://api.mailgun.net/v3/{}/messages'
        url = url.format(MAILGUN_DOMAIN_NAME)
        auth = ('api', MAILGUN_API_KEY)
        dados = {
            'from': 'Mailgun User <postmaster@{}>'.format(MAILGUN_DOMAIN_NAME),
            'to': destino,
            'subject': 'Tapioca do Billy - Seu produto está disponível',
            'text': corpo
        }

        response = requests.post(url, auth=auth, data=dados)
        response.raise_for_status()


if __name__ == '__main__':
    app.run()
