class Compra:
    def __init__(self, dt, num, taxa, end_entrega, produtos):
        self.data = dt
        self.numero = num
        self.taxa = taxa
        self.endereco_entrega = end_entrega
        self.produtos = produtos
