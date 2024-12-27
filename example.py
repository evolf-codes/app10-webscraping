import sqlite3

connection = sqlite3.connect("db_data.db")
cursor = connection.cursor()

res = cursor.execute("SELECT * FROM events").fetchall()

print(res)

new_rows =[('Cats','Cat City','2088-1-1')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()

res = cursor.execute("SELECT * FROM events").fetchall()

print(res)