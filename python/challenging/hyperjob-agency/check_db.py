import sqlite3
con = sqlite3.connect("db.hyperjob.sqlite3")
cursor = con.cursor()
cursor.execute("SELECT * FROM vacancy_vacancy;")
print(cursor.fetchall())
