import sqlite3

conn = sqlite3.connect("infra.db")
c = conn.cursor()

# CREATE AUTH TABLE (NEW NAME)
c.execute("""
CREATE TABLE IF NOT EXISTS auth_users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# DEFAULT ADMIN ACCOUNT
c.execute("""
INSERT OR IGNORE INTO auth_users (email,password)
VALUES ('ITadmin@infraon.io','admin1234')
""")

conn.commit()
conn.close()

print("Authentication system installed successfully")