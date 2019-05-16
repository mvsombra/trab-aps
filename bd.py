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

    def produtos_mais_vendidos(self, item=True, valor=True, qtd=1, cat=None):
        if(item):
            q = "SELECT * FROM produto WHERE cod in (select cod from " \
                "(select cod, count(item) from produto inner join " \
                "produto_vendido on item=cod {}group by cod order by " \
                "count desc limit {}) as tb);"
        else:
            q = "SELECT * FROM produto WHERE cod in (SELECT cod FROM " \
                "(SELECT cod, SUM(preco) FROM produto INNER JOIN " \
                "produto_vendido ON item=cod {}GROUP BY cod ORDER BY " \
                "SUM DESC LIMIT {}) AS tb);"

        if(cat == 0 or cat == 1):
            s = "WHERE tipo={} ".format(cat)
            q = q.format(s, qtd)
        else:
            q = q.format('', qtd)
        # realiza a busca e retorna
        self.db.cur.execute(q)
        return self.db.cur.fetchall()

    def select_produtos(self, ultimos=0, busca=None, cod=None, cat=None):
        q = "SELECT * FROM produto {}"

        if(cat == 0 or cat == 1):
            q = q.format("WHERE tipo={} ".format(cat))
        elif(busca):
            busca = '%' + busca.lower() + '%'
            ultimos = 0
            q = q.format("WHERE LOWER(nome) LIKE '{}' ".format(busca))
        elif(cod):
            q = q.format("WHERE cod='{}' ".format(cod))
        else:
            q = q.format('')

        # limita os resultados ou não
        if(ultimos > 0):
            q += " LIMIT {};".format(ultimos)
        else:
            q += ';'

        # realiza a busca e retorna
        self.db.cur.execute(q)
        return self.db.cur.fetchall()

    def select_notificacao(self):
        q = "SELECT cliente FROM notificacao INNER JOIN produto ON cod=prod " \
            "WHERE disponibilidade='True' GROUP BY cliente;"
        # realiza a busca e retorna
        self.db.cur.execute(q)
        return self.db.cur.fetchall()

    def select_carrinho(self, user):
        q = "SELECT cod, preco, disponibilidade, nome, tipo, descricao, " \
            "count(prod) FROM produto INNER JOIN carrinho ON cod=prod WHERE " \
            "cliente='{}' group by cod;".format(user)
        # realiza a busca e retorna
        self.db.cur.execute(q)
        return self.db.cur.fetchall()

    def delete_carrinho(self, cliente, prod):
        q = "DELETE FROM carrinho WHERE prod='{}' AND cliente='{}';"
        q = q.format(prod, cliente)
        self.db.cur.execute(q)
        self.db.conn.commit()

    def delete_notificacao(self):
        q = "DELETE FROM notificacao WHERE prod IN (SELECT cod FROM produto " \
            "WHERE disponibilidade='true');"
        self.db.cur.execute(q)
        self.db.conn.commit()

    def esvaziar_carrinho(self, cliente):
        q = "DELETE FROM carrinho WHERE cliente='{}';".format(cliente)
        self.db.cur.execute(q)
        self.db.conn.commit()

    def insert_notificacao(self, cod, prod):
        q = "INSERT INTO notificacao VALUES ('{}', '{}');".format(cod, prod)
        self.db.cur.execute(q)
        self.db.conn.commit()

    def insert_carrinho(self, cliente, prod):
        q = "INSERT INTO carrinho VALUES ('{}', '{}');".format(prod, cliente)
        self.db.cur.execute(q)
        self.db.conn.commit()

    def insert_user(self, nome, cpf, dt_nasc, telefone, endereco,
                    email, senha):
        q = "INSERT INTO usuario VALUES ('{}', '{}', '{}', '{}', '{}', " \
            "'{}', '{}', 0);"
        q = q.format(nome, cpf, dt_nasc, telefone, endereco, email, senha)

        self.db.cur.execute(q)
        self.db.conn.commit()

    def insert_produto(self, cod, nome, preco, disp, tipo, desc):
        q = "INSERT INTO produto VALUES ('{}', {}, {}, '{}', {}, '{}');"
        q = q.format(cod, preco, disp, nome, tipo, desc)
        print(q)

        self.db.cur.execute(q)
        self.db.conn.commit()

    def update_produto(self, cod, nome, preco, disp, tipo, desc):
        q = "UPDATE produto SET nome='{}', preco={}, disponibilidade={}, " \
            "tipo={}, descricao='{}' WHERE cod='{}';"
        q = q.format(nome, preco, disp, tipo, desc, cod)

        self.db.cur.execute(q)
        self.db.conn.commit()

    def auth_user(self, email, senha):
        senha_user = self.select_users(email=email, max_results=1)[6]
        return senha == senha_user
