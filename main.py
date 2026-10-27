import sqlite3

conexao = sqlite3.connect("estoque.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco REAL NOT NULL CHECK(preco >= 0),
        quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
        estoque_minimo INTEGER NOT NULL CHECK(estoque_minimo >= 0)
    )
""")

conexao.commit()

def cadastrar_produto(nome, categoria, preco, qntd, estoque):

    cursor.execute("""
        INSERT INTO produtos (nome, categoria, preco, quantidade, estoque_minimo)
        VALUES (?,?,?,?,?)
    """,(nome, categoria, preco, qntd, estoque))

    conexao.commit()

def listar_todos_produtos():

    cursor.execute("""
        SELECT *
        FROM produtos
    """)
    produtos = cursor.fetchall()
    for prod in produtos:
        print(prod)

def buscar_produto(nome):

    cursor.execute("""
        SELECT *
        FROM produtos
        WHERE nome LIKE ?
    """, (f"%{nome}%",))
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum produto encontrado")
    else:
        for r in resultado:
            print(r)

def atualizar_estoque(id):

    cursor.execute("""
        SELECT id
        FROM produtos
        WHERE id = ?
    """, (id,))
    resultado = cursor.fetchone()
    if(resultado is None): 
        print("Produto não encontrado")
        return

    opcao = ""
    while(opcao not in ("0","1")):
        opcao = input("Adicionar [0] ou Remover [1]: ")

    if(opcao == "0"): 

        adicionar = 0
        while(adicionar < 1):
            adicionar = int(input("Adicionar quantas unidades: "))
            if(adicionar < 1): print("Insira um valor válido")
        cursor.execute("""
                UPDATE produtos
                SET quantidade = quantidade + ?
                WHERE id = ?
            """, (adicionar, id))
        
    else:
        cursor.execute("""
            SELECT quantidade
            FROM produtos
            WHERE id = ?
        """, (id,))
        qntd = cursor.fetchone()[0] # pega a quantidade atual 
        if(qntd > 0):
            remover = 0
            while(remover < 1):
                remover = int(input("Remover quantas unidades: "))
                if(remover < 1): print("Insira um valor válido")
            if(qntd >= remover):
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade = quantidade - ?
                    WHERE id = ?
                """, (remover, id))
            else: print(f"Não é possível remover {remover} unidades. Unidades disponíveis = {qntd}")
        else: print("Não há produto no estoque")

    conexao.commit()

def excluir_produto(id):

    cursor.execute("""
        SELECT id
        FROM produtos
        WHERE id = ?
    """, (id,))
    resultado = cursor.fetchone()
    if(resultado is None): 
        print("Produto não encontrado")
        return

    cursor.execute("""
        SELECT nome
        FROM produtos
        WHERE id = ?
    """, (id,))
    nome = cursor.fetchone()[0]

    confimacao = ""
    while(confimacao not in ("0","1")):
        confimacao = input(f'CONFIRMAÇÃO - Excluir produto "{nome}": Ignorar [0] ou Confirmar [1]: ')
        if(confimacao not in ("0","1")): print("Opção inválida")

    if(confimacao == "1"): 
        cursor.execute("""
            DELETE FROM produtos
            WHERE id = ?
        """, (id,))
    else: return

    conexao.commit()

def consultar_estoque_baixo():
    cursor.execute("""
        SELECT *
        FROM produtos
        WHERE quantidade <= estoque_minimo
    """)
    produtos_alerta = cursor.fetchall()
    for prod in produtos_alerta:
        print(prod)
        

def relatorio_estoque():
    # COALESCE está transformando null em zero
    cursor.execute("""
        SELECT COUNT(id), COALESCE(SUM(quantidade),0), COALESCE(SUM(preco * quantidade),0) 
        FROM produtos 
    """)
    resultado = cursor.fetchone()
    print(f"Quantidade de produtos diferentes cadastrados = {resultado[0]}")
    print(f"Quantidade total de unidades em estoque = {resultado[1]}")
    print(f"Valor financeiro total do estoque = {resultado[2]}")

    cursor.execute("""
        SELECT COUNT(*)
        FROM produtos
        WHERE quantidade <= estoque_minimo
    """)
    qtd_prod_abaixo = cursor.fetchone()[0]
    print(f"Quantidade de produtos com estoque baixo = {qtd_prod_abaixo}")
    

    cursor.execute("""
        SELECT nome, preco
        FROM produtos
        WHERE preco = (SELECT MAX(preco) FROM produtos)
    """)
    prod_mais_caro = cursor.fetchall()
    for nome, preco in prod_mais_caro:
        print(f"Produto mais caro = {nome} ({preco:.2f} Reais)")

# Interface terminal  

while(True):
    print("========== STOCKPY ==========")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Buscar produto")
    print("4 - Atualizar estoque")
    print("5 - Excluir produto")
    print("6 - Consultar estoque baixo")
    print("7 - Relatório de estoque")
    print("0 - Sair")
    print("=============================")
    print("\n")

    resposta = input("Escolha uma opção: ")

    match resposta:
        case "0":
            print("Programa encerrado")
            break
        case "1":
            nome_produto = ""
            while(nome_produto == ""):
                nome_produto = input("Nome do produto: ").strip() # strip garante que espaços em brancos também seja considerado vazio
            
            categoria_produto = ""
            while(categoria_produto == ""):
                categoria_produto = input("Categoria do produto: ").strip()

            preco_produto = -1
            while(preco_produto < 0): 
                preco_produto = float(input("Preço do produto: "))

            quantidade_produto = -1
            while(quantidade_produto < 0):
                quantidade_produto = int(input("Quantide de produtos: "))

            estoque_minimo_produto = -1
            while(estoque_minimo_produto < 0):
                estoque_minimo_produto = int(input("Estoque mínimo do produto: "))

            cadastrar_produto(nome_produto, categoria_produto, preco_produto, quantidade_produto, estoque_minimo_produto)
            print("Produto Cadastrado com Sucesso!")

        case "2":
            listar_todos_produtos()
        case "3":
            nome_produto = ""
            while(nome_produto == ""):
                nome_produto = input("Nome do produto: ").strip()
            buscar_produto(nome_produto)
        case "4":
            id_produto = 0
            while(id_produto < 1):
                id_produto = int(input("Id do produto: "))
            atualizar_estoque(id_produto)
        case "5":
            id_produto = 0
            while(id_produto < 1):
                id_produto = int(input("Id do produto: "))
            excluir_produto(id_produto)
        case "6":
            consultar_estoque_baixo()
        case "7":
            relatorio_estoque()
        case _: 
            print("Opção inválida")

conexao.close()



