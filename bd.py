import pickle
import psycopg2


class BancoDados:
    def __init__(self):
        comando = pickle.load(open('loginbd.pkl', 'rb'))

        self.conn = psycopg2.connect(comando, sslmode='require')
        self.cur = self.conn.cursor()


class AcessoBD:
    def __init__(self):
        self.db = BancoDados()

    def select_users(self, nome=None, email=None, max_results=0):
        q = "SELECT * FROM usuario {}ORDER BY nome;"
        if(email):
            q = q.format("WHERE email='{}' ".format(email))
        elif(nome):
            q = q.format("WHERE nome='{}' ".format(nome))
        else:
            q = q.format('')
        # executa a busca
        self.db.cur.execute(q)
        # limita os resultados e retorna
        if(max_results == 1):
            return self.db.cur.fetchall()[0]
        elif(max_results > 1):
            return self.db.cur.fetchall()[:max_results]
        else:
            return self.db.cur.fetchall()

    def auth_user(self, email, senha):
        senha_user = self.select_users(email=email, max_results=1)[6]
        return senha == senha_user
