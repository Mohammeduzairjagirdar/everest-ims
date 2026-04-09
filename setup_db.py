import sqlite3

conn = sqlite3.connect("infra.db")
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS auth_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)""")

# Insert user
c.execute("INSERT OR IGNORE INTO auth_users (email, password) VALUES (?, ?)",
          ("itadmin@infraon.io", "admin1234"))

conn.commit()

# Verify
c.execute("SELECT * FROM auth_users")
rows = c.fetchall()
print("Users in DB:")
for row in rows:
    print(row)

conn.close()
