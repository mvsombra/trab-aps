from flask import Flask
from desenha_tela import DesenhaTela as dt

app = Flask(__name__)
draw = dt()


@app.route('/')
def index():
    return draw.render('index')


@app.route('/ver-produto')
def ver_produto():
    return draw.render('ver-produto')


if __name__ == '__main__':
    app.run()
