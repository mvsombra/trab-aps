class Produto:
    def __init__(self, cod, preco, disp, nome, tipo):
        self.codigo = cod
        self.preco = preco
        self.disponibilidade = disp
        self.nome = nome
        self.tipo = tipo

    @property
    def esta_disponivel(self):
        return self.disponibilidade

    def alterar_disponibilidade(self):
        self.disponibilidade = not self.disponibilidade
