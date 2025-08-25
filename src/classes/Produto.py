class Produto:
    lista_produtos = []

    def __init__(self, id: int, nome: str, quantidade, preco: float = 0.0):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
    
    def __str__(self):
        return f"Código: {self.id} | Produto: {self.nome} | Quantidade: {self.quantidade} | Valor: R$ {self.preco:.2f}"
    
    def cadastrar_produto(self):
        try:
                id = int(input("Código do produto: "))
                nome = str(input("Nome do produto: "))
                quantidade = int(input("Quantidade em estoque: "))
                preco = float(input("Preço do produto: "))
                produto = Produto(id, nome, quantidade, preco)
                self.lista_produtos.append(produto)
                return "Produto cadastrado com sucesso."
        except IndexError:
            print("Não há nenhum índice")
        except ValueError:
            print("Dica: verifique se você digitou apenas números inteiros para código/quantidade e número decimal para preço.")

    
    def listar_estoque(self):
        if not self.lista_produtos:
            return print("Nenhum produto cadastrado!")
        for produto in self.lista_produtos:
            print(produto)