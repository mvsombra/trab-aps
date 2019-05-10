from flask import Flask, request, g, session, redirect, url_for
from sessions import RedisSessionInterface
from desenha_tela import DesenhaTela as dt
from bd import AcessoBD

dba = AcessoBD()
app = Flask(__name__)
app.session_interface = RedisSessionInterface()
draw = dt()


@app.route('/')
def index():
    return draw.render('index')


@app.route('/ver-produto')
def ver_produto():
    return draw.render('ver-produto')


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if(request.method == 'POST'):
        return "Produto adicionado"
    else:
        return draw.render('carrinho')


@app.route('/notificacao', methods=['GET', 'POST'])
def notificacao():
    return "Notificação atividada"


@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if(g.user):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        session.pop('user', None)
        return str(dba.auth_user(request.form['email'], request.form['senha']))
    return draw.render('login')


@app.route('/cadastrar')
def cadastrar():
    return draw.render('cadastro')


@app.before_request
def before_request():
    g.user = None
    if('user' in session):
        g.user = session['user']


if __name__ == '__main__':
    app.run()
