class Produto:

    def __init__(self, id: int, nome: str, quantidade, preco: float = 0.0):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
    
    def __str__(self):
        return f"Código: {self.id} | Produto: {self.nome} | Quantidade: {self.quantidade} | Valor: R$ {self.preco:.2f}"
