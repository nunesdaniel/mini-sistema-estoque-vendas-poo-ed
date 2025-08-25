import os, sys, time

from src.classes.Produto import Produto

def cls():
    time.sleep(0.4)
    choice = input("Pressione Enter para continuar")
    os.system("CLS" if os.name == "nt" else "clear")

def main_menu():
    while True:
        cls()
        print(
            "===== Menu principal =====\n"
            "1 - Clientes\n"
            "2 - Estoque\n"
            "3 - Sair"
            )
        choice = input("\nPor favor, escolha a opção desejada: ").strip()
        match choice:
            case "1":
                print("")
                client_menu()
            case "2":
                print("")
                inventory_menu()
            case "3":
                print("Até mais!\n")
                sys.exit()
            case _:
                print("Opção inválida!")

def client_menu():
    while True:
        cls()
        print(
            "===== Menu Clientes =====\n"
            "1 - Cadastrar cliente\n"
            "2 - Listar clientes\n"            
            "3 - Exibir clientes e valores totais gastos\n"
            "4 - Voltar"
            )
        choice = input("\nEscolha: ").strip()
        match choice:
            case "1":
                print("")
            case "2":
                print("")
            case "3":
                print("")
            case "4":
                print("Voltando...\n")
                break
            case _:
                print("Opção inválida!")
    

def inventory_menu():
    while True:
        cls()
        print(
            "===== Menu Estoque =====\n"
            "1 - Cadastrar Produto\n"
            "2 - Listar produtos\n"
            "3 - Realizar venda\n"
            "4 - Ver fila de vendas\n"
            "5 - Desfazer última operação\n"
            "6 - Exibir valor total do estoque\n"
            "7 - Exibir valor total de vendas realizadas\n"
            "8 - Voltar"
            )
        choice = input("\nEscolha: ").strip()
        match choice:
            case "1":
                print("")
                Produto.cadastrar_produto(Produto)
            case "2":
                print("")
                Produto.listar_estoque(Produto)
            case "3":
                print("")
            case "4":
                print("")
            case "5":
                print("")
            case "6":
                print("")
            case "7":
                print("")
            case "8":
                print("Voltando...\n")
                break
            case _:
                print("Opção inválida!")

def main():
    main_menu()

if __name__ == "__main__":
    main()