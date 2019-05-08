class Usuario:
    def __init__(self, nome, cpf, dt_nasc, telefone, endereco, email, senha,
                 permissao):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = dt_nasc
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha
        self.permissao = permissao


class Admin(Usuario):
    def __init__(self, nome, cpf, dt_nasc, telefone, endereco, email, senha):
        super().__init__(nome, cpf, dt_nasc, telefone, endereco, email,
                         senha, 1)


class Cliente(Usuario):
    def __init__(self, nome, cpf, dt_nasc, telefone, endereco, email, senha):
        super().__init__(nome, cpf, dt_nasc, telefone, endereco, email,
                         senha, 0)
        self.carrinho = []
        self.compras = []
