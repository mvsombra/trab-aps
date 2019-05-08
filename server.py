from flask import Flask, request
from desenha_tela import DesenhaTela as dt

app = Flask(__name__)
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


@app.route('/entrar')
def entrar():
    return draw.render('login')


@app.route('/cadastrar')
def cadastrar():
    return draw.render('cadastro')


if __name__ == '__main__':
    app.run()
