import sqlite3, os

# Remove lock files
for f in ["infra.db", "infra.db-wal", "infra.db-shm"]:
    if os.path.exists(f):
        os.remove(f)
        print(f"Deleted {f}")

# Create fresh DB
conn = sqlite3.connect("infra.db")
cur = conn.cursor()

cur.execute("PRAGMA journal_mode=WAL")

cur.execute("""CREATE TABLE IF NOT EXISTS servers (
    server_id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_ip TEXT, server_name TEXT, server_type TEXT,
    total_cpu INTEGER, total_ram INTEGER, total_storage INTEGER, status TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS vm_requests (
    vm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vm_name TEXT, team_name TEXT, server_id INTEGER,
    ip_address TEXT, cpu_required INTEGER, ram_required INTEGER,
    storage_required INTEGER, purpose TEXT, approval_status TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS ip_pool (
    ip_address TEXT PRIMARY KEY, ip_status TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS auth_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE, password TEXT
)""")

cur.execute("INSERT OR IGNORE INTO auth_users (email, password) VALUES ('ITadmin@infraon.io', 'admin1234')")
conn.commit()
conn.close()
print("✅ Fresh database created!")
print("Login: ITadmin@infraon.io / admin1234")
