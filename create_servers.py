import sqlite3

conn = sqlite3.connect("infra.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS servers(
    server_id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_name TEXT,
    total_cpu INTEGER,
    total_ram INTEGER,
    total_storage INTEGER,
    status TEXT
)
""")

cur.execute("""
INSERT OR IGNORE INTO servers(server_id, server_name, total_cpu, total_ram, total_storage, status)
VALUES
(1,'Prod-Server-01',32,128,2000,'Active'),
(2,'Prod-Server-02',24,96,1500,'Active'),
(3,'Dev-Server-01',16,64,1000,'Active'),
(4,'Test-Server-01',8,32,500,'Active')
""")

conn.commit()
conn.close()

print("Servers table created")