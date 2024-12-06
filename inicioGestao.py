import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

#criando tabelas

conn = sqlite3.connect('estoque.db')

cursor = conn.cursor()

cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS conteudo (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      produto TEXT NOT NULL,
      classe TEXT NOT NULL,
      quantidade INTEGER NOT NULL,
      preço REAL NOT NULL,
      local TEXT NOT NULL
     )
''')

# Função para obter os dados do banco de dados
def obter_dados():
    conn = sqlite3.connect('estoque.db')
    df = pd.read_sql_query('SELECT * FROM conteudo', conn)
    conn.close()
    return df

# Função para adicionar um produto ao banco de dados
def adicionar_produto(produto, classe, quantidade, preco, local):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conteudo (produto, classe, quantidade, preço, local)
        VALUES (?, ?, ?, ?, ?)
    ''', (produto, classe, quantidade, preco, local))
    conn.commit()
    conn.close()
    atualizar_dados()

# Função para remover um produto do banco de dados
def remover_produto(id_produto):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM conteudo WHERE id = ?
    ''', (id_produto,))
    conn.commit()
    conn.close()
    atualizar_dados()

# Função para mostrar os dados na interface gráfica
def mostrar_dados():
    df = obter_dados()

    # Interface
    root = tk.Tk()
    root.title("Estoque de equipamentos")

    # Treeview para exibir os dados
    tree = ttk.Treeview(root, columns=list(df.columns), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for coluna in df.columns:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, width=100)

    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    # Função para adicionar um novo produto
    def callback_adicionar():
        produto = entry_produto.get()
        classe = entry_classe.get()
        quantidade = int(entry_quantidade.get())
        preco = float(entry_preco.get())
        local = entry_local.get()
        adicionar_produto(produto, classe, quantidade, preco, local)

    # Função para remover o produto selecionado
    def callback_remover():
        try:
            selected_item = tree.selection()[0]
            id_produto = tree.item(selected_item)['values'][0]
            remover_produto(id_produto)
        except IndexError:
            messagebox.showerror("Erro", "Selecione um produto para remover.")

    # Função para mostrar a localização do produto selecionado
    def callback_mostrar_local():
        try:
            selected_item = tree.selection()[0]
            local = tree.item(selected_item)['values'][-1]
            messagebox.showinfo("Localização do Produto", f"O produto está localizado em: {local}")
        except IndexError:
            messagebox.showerror("Erro", "Selecione um produto para ver o local.")

    # Campos para adicionar um novo produto
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Produto").grid(row=0, column=0)
    entry_produto = tk.Entry(frame)
    entry_produto.grid(row=0, column=1)

    tk.Label(frame, text="Classe").grid(row=0, column=2)
    entry_classe = tk.Entry(frame)
    entry_classe.grid(row=0, column=3)

    tk.Label(frame, text="Quantidade").grid(row=1, column=0)
    entry_quantidade = tk.Entry(frame)
    entry_quantidade.grid(row=1, column=1)

    tk.Label(frame, text="Preço").grid(row=1, column=2)
    entry_preco = tk.Entry(frame)
    entry_preco.grid(row=1, column=3)

    tk.Label(frame, text="Local").grid(row=2, column=0)
    entry_local = tk.Entry(frame)
    entry_local.grid(row=2, column=1)

    # Botões para adicionar, remover e ver o local do produto
    btn_adicionar = tk.Button(frame, text="Adicionar Produto", command=callback_adicionar)
    btn_adicionar.grid(row=3, column=0, pady=5)

    btn_remover = tk.Button(frame, text="Remover Produto", command=callback_remover)
    btn_remover.grid(row=3, column=1, pady=5)

    btn_mostrar_local = tk.Button(frame, text="Mostrar Local", command=callback_mostrar_local)
    btn_mostrar_local.grid(row=3, column=2, pady=5)

    root.mainloop()

# Função para atualizar os dados na interface gráfica
def atualizar_dados():
    mostrar_dados()

mostrar_dados()
