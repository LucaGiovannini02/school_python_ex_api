import sqlite3 as sq

conn = sq.connect('CarteFedelta.sqlite3')

with open('db.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

cur.execute("SELECT * FROM TCarteFedelta INNER JOIN TMovimenti ON TCarteFedelta.CartaFedeltaID = TMovimenti.CartaFedeltaID INNER JOIN TPremi ON TMovimenti.PremioID = TPremi.PremioID")
data = cur.fetchall()
print(data)

conn.commit()
conn.close()