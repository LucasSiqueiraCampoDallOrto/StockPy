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

