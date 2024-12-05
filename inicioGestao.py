import sqlite3

conn = sqlite3.connect('estoque.db')

cursor = conn.cursor()

cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS conteudo (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      produto TEXT NOT NULL,
      classe TEXT NOT NULL,
      quantidade INTEGER NOT NULL
     )
''')

cursor.execute('''
 INSERT INTO conteudo (produto, classe, quantidade)
 VALUES (?, ?, ?)
''', ('Notebook', 'A', 300))

conn.commit()

cursor.execute('SELECT * FROM conteudo')
conteudo = cursor.fetchall()
print(conteudo)

conn.close()




