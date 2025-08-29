import os, sys, time
from collections import deque
from src.classes.Produto import Produto
from src.classes.Cliente import Cliente

# ===== Estruturas de dados =====
produtos = []              # LISTA do estoque
clientes = Cliente.carregar_todos()
fila_vendas = deque()      # FILA de vendas (ordem de chegada) - agora inclui cliente_id
pilha_desfazer = []        # PILHA para desfazer última operação

def cls():
    time.sleep(0.4)
    input("Pressione Enter para continuar")
    os.system("CLS" if os.name == "nt" else "clear")

# ---------- Persistência em TXT ----------
def _garante_pasta():
    os.makedirs("dados", exist_ok=True)

def salvar_estoque_txt():
    _garante_pasta()
    with open("dados/estoque.txt", "w", encoding="utf-8") as f:
        for p in produtos:
            f.write(f"{p.id};{p.nome};{p.quantidade};{p.preco}\n")

def carregar_estoque_txt():
    caminho = "dados/estoque.txt"
    if not os.path.exists(caminho):
        return
    produtos.clear()
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            pid, nome, qtd, preco = linha.split(";")
            produtos.append(Produto(int(pid), nome, int(qtd), float(preco)))

def salvar_vendas_txt():
    _garante_pasta()
    with open("dados/vendas.txt", "w", encoding="utf-8") as f:
        for v in fila_vendas:
            # Agora persistimos também o cliente_id (obrigatório)
            f.write(f'{v["produto_id"]};{v["nome"]};{v["quantidade"]};{v["valor_total"]};{v["cliente_id"]}\n')

def carregar_vendas_txt():
    caminho = "dados/vendas.txt"
    if not os.path.exists(caminho):
        return
    fila_vendas.clear()
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(";")
            # Backcompat: se arquivo antigo (sem cliente_id), ignora a linha (ou trate como inválida)
            if len(partes) == 5:
                pid, nome, qtd, vt, cid = partes
                fila_vendas.append({
                    "produto_id": int(pid),
                    "nome": nome,
                    "quantidade": int(qtd),
                    "valor_total": float(vt),
                    "cliente_id": int(cid)
                })
            else:
                # se quiser aceitar arquivo antigo, poderia atribuir cliente_id=0; aqui vamos ignorar por segurança
                continue

def salvar_tudo():
    salvar_estoque_txt()
    salvar_vendas_txt()

# ---------- Utilitário ----------
def encontrar_produto_por_id(pid: int):
    for p in produtos:
        if p.id == pid:
            return p
    return None

def encontrar_cliente_por_id(cid: int):
    for c in clientes:
        if c.id == cid:
            return c
    return None

# ---------- Menus ----------
def menu_principal():
    while True:
        cls()
        print(
            "===== Menu principal =====\n"
            "1 - Clientes\n"
            "2 - Estoque\n"
            "3 - Sair"
        )
        escolha = input("\nPor favor, escolha a opção desejada: ").strip()
        match escolha:
            case "1":
                print("")
                menu_cliente()
            case "2":
                print("")
                menu_estoque()
            case "3":
                print("Até mais!\n")
                sys.exit()
            case _:
                print("Opção inválida!")

def menu_cliente():
    while True:
        cls()
        print(
            "===== Menu Cliente =====\n"
            "1 - Cadastrar cliente\n"
            "2 - Listar clientes\n"
            "3 - Exibir clientes e valores totais gastos\n"
            "4 - Voltar"
        )
        escolha = input("\nPor favor, escolha a opção desejada: ").strip()

        match escolha:
            case "1":
                nome = input("Nome do cliente: ").strip()
                if not nome:
                    print("Nome não pode ser vazio!")
                else:
                    Cliente.adicionar(clientes, nome)
                    print("Cliente cadastrado com sucesso!")
            case "2":
                if not clientes:
                    print("Nenhum cliente cadastrado.")
                else:
                    print("\n=== Clientes ===")
                    for c in clientes:
                        print(f"{c.id} - {c.nome}")
            case "3":
                if not clientes:
                    print("Nenhum cliente cadastrado.")
                else:
                    print("\n=== Clientes e valores totais gastos ===")
                    for c in clientes:
                        print(f"{c.id} - {c.nome}: R$ {c.total_gasto:.2f}")
            case "4":
                return
            case _:
                print("Opção inválida!")

def menu_estoque():
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
        escolha = input("\nEscolha: ").strip()
        match escolha:
            case "1":
                try:
                    pid = int(input("Código do produto: "))
                    if encontrar_produto_por_id(pid):
                        print("Já existe um produto com esse ID.")
                    else:
                        nome = input("Nome do produto: ")
                        quantidade = int(input("Quantidade em estoque: "))
                        preco = float(input("Preço do produto: "))
                        p = Produto(pid, nome, quantidade, preco)
                        produtos.append(p)
                        pilha_desfazer.append(("remover_produto", {"produto_id": pid}))
                        salvar_tudo()
                        print("Produto cadastrado com sucesso.")
                except ValueError:
                    print("Dica: código/quantidade = inteiros; preço = decimal.")
            case "2":
                if not produtos:
                    print("Nenhum produto cadastrado no estoque.")
                else:
                    for produto in produtos:
                        try:
                            print(produto)
                        except Exception:
                            print(f"ID: {produto.id} | Nome: {produto.nome} | Quantidade: {produto.quantidade} | Preço: R${produto.preco:.2f}")
            case "3":
                try:
                    pid = int(input("Digite o ID do produto: "))
                    qtd = int(input("Digite a quantidade: "))
                    produto = encontrar_produto_por_id(pid)
                    if not produto:
                        print("Produto não encontrado.")
                    elif qtd <= 0:
                        print("Quantidade inválida.")
                    elif produto.quantidade < qtd:
                        print("Estoque insuficiente.")
                    else:
                        # ---- ID do cliente: OBRIGATÓRIO ----
                        cid = int(input("Digite o ID do cliente: "))
                        cliente = encontrar_cliente_por_id(cid)
                        if not cliente:
                            print("Cliente não encontrado. Operação cancelada.")
                        else:
                            produto.quantidade -= qtd
                            valor_total = qtd * produto.preco

                            # atualiza total gasto do cliente (obrigatório)
                            cliente.registrar_compra(valor_total)
                            Cliente.salvar_todos(clientes)

                            venda = {
                                "produto_id": pid,
                                "nome": produto.nome,
                                "quantidade": qtd,
                                "valor_total": valor_total,
                                "cliente_id": cid
                            }
                            fila_vendas.append(venda)
                            pilha_desfazer.append(("desfazer_venda", venda))
                            salvar_tudo()
                            print(f"Venda realizada com sucesso! (Valor total: R${valor_total:.2f})")
                except ValueError:
                    print("Dica: IDs e quantidades são inteiros.")
            case "4":
                if not fila_vendas:
                    print("Fila de vendas vazia.")
                else:
                    print("--- FILA DE VENDAS ---")
                    for v in fila_vendas:
                        print(
                            f'Produto: {v["nome"]} | Quantidade: {v["quantidade"]} | '
                            f'Valor Total: R${v["valor_total"]:.2f} | Cliente ID: {v["cliente_id"]}'
                        )
            case "5":
                if not pilha_desfazer:
                    print("Nada a desfazer.")
                else:
                    op, payload = pilha_desfazer.pop()
                    if op == "remover_produto":
                        pid = payload["produto_id"]
                        prod = encontrar_produto_por_id(pid)
                        if prod:
                            produtos.remove(prod)
                            print('Última operação desfeita! (cadastro de produto cancelado)')
                        else:
                            print("Nada a remover (produto não existe mais).")
                    elif op == "desfazer_venda":
                        venda = payload
                        prod = encontrar_produto_por_id(venda["produto_id"])
                        if prod:
                            prod.quantidade += venda["quantidade"]
                        # reverte total gasto do cliente
                        cli = encontrar_cliente_por_id(venda.get("cliente_id", 0))
                        if cli:
                            cli.registrar_compra(-float(venda["valor_total"]))
                            Cliente.salvar_todos(clientes)
                        try:
                            fila_vendas.remove(venda)
                        except ValueError:
                            if fila_vendas:
                                fila_vendas.pop()
                        print('Última operação desfeita com sucesso! (venda cancelada)')
                    salvar_tudo()
            case "6":
                total = sum(p.quantidade * p.preco for p in produtos)
                print(f"Valor total do estoque: R${total:.2f}")
            case "7":
                total_vendas = sum(v["valor_total"] for v in fila_vendas)
                print(f"Valor total de vendas realizadas: R${total_vendas:.2f}")
            case "8":
                print("Voltando...\n")
                break
            case _:
                print("Opção inválida!")

def main():
    # carrega dados salvos (se existirem)
    carregar_estoque_txt()
    carregar_vendas_txt()
    menu_principal()

if __name__ == "__main__":
    main()
