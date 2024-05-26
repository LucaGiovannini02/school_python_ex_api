import sqlite3 as sq

conn = sq.connect('CarteFedelta.sqlite3')

with open('db.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

conn.execute("INSERT INTO TPremi (Nome, PuntiMinimi) VALUES ('Macchina', '20')")
conn.execute("INSERT INTO TPremi (Nome, PuntiMinimi) VALUES ('Moto', '10')")

conn.commit()

conn.commit()
conn.close()