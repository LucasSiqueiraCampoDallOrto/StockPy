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
    if resultado is None:
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

    cursor.execute("""
        SELECT COUNT(id), SUM(quantidade), SUM(preco * quantidade)
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


