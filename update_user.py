import sqlite3
conn = sqlite3.connect('infra.db')
conn.execute("DELETE FROM auth_users")
conn.execute("INSERT INTO auth_users (email, password) VALUES ('itadmin@infraon.io', 'admin1234')")
conn.commit()
users = conn.execute("SELECT * FROM auth_users").fetchall()
print("Done! Current users:", users)
conn.close()