import sqlite3 as sq

conn = sq.connect('CarteFedelta.sqlite3')

with open('db.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

conn.commit()
conn.close()