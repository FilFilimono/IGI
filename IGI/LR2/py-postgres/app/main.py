import psycopg2
import time


time.sleep(5)

conn = psycopg2.connect(
    host="db",
    database="mydb",
    user="myuser",
    password="mypassword"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        grade INT
    )
""")

cur.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", ("Alice", 90))
cur.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", ("Bob", 85))

conn.commit()

cur.execute("SELECT * FROM students")
rows = cur.fetchall()

print("Students in database:")
for row in rows:
    print(f"  id={row[0]}, name={row[1]}, grade={row[2]}")

cur.close()
conn.close()