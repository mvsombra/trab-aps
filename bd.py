import pickle
import psycopg2


class BancoDados:
    def __init__(self):
        comando = pickle.load(open('loginbd.pkl', 'rb'))

        self.conn = psycopg2.connect(comando, sslmode='require')
        self.cur = self.conn.cursor()


class AcessoBD:
    def __init__(self):
        self.bd = BancoDados()
