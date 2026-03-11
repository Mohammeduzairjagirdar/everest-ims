import sqlite3

conn = sqlite3.connect("infra.db")
cur = conn.cursor()

# ----------------- CREATE TABLES -----------------

cur.execute("""
CREATE TABLE IF NOT EXISTS ip_pool(
    ip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT UNIQUE,
    ip_status TEXT,
    vm_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS vm_requests(
    vm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vm_name TEXT,
    team_name TEXT,
    server_id INTEGER,
    ip_address TEXT,
    cpu_required INTEGER,
    ram_required INTEGER,
    storage_required INTEGER,
    purpose TEXT,
    approval_status TEXT
)
""")

# ----------------- CLEAR OLD DATA -----------------

cur.execute("DELETE FROM ip_pool")

# ----------------- INSERT 20 IPs -----------------

# first 15 = assigned
# last 5 = free

for i in range(1, 21):

    ip = f"192.168.10.{i}"

    if i <= 15:
        status = "assigned"
    else:
        status = "free"

    cur.execute(
        "INSERT INTO ip_pool (ip_address, ip_status) VALUES (?,?)",
        (ip, status)
    )

conn.commit()
conn.close()

print("Database seeded successfully!")
print("20 IPs added → 15 assigned + 5 free")
