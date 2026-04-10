import sqlite3

conn = sqlite3.connect("infra.db")
cur = conn.cursor()

# ---------------- SERVERS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS servers (
    server_id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_ip TEXT,
    server_name TEXT,
    server_type TEXT,
    total_cpu INTEGER,
    total_ram INTEGER,
    total_storage INTEGER,
    status TEXT
)
""")

# Insert default servers only if empty
cur.execute("SELECT COUNT(*) FROM servers")
if cur.fetchone()[0] == 0:
    servers_data = [
        ("192.168.51.1", "Host-01", "KVM",        32, 128, 500, "active"),
        ("192.168.51.2", "Host-02", "VMware",      48, 256, 500, "active"),
        ("192.168.51.3", "Host-03", "Hypervisor",  24, 64,  500, "active"),
    ]
    cur.executemany(
        "INSERT INTO servers(host_ip, server_name, server_type, total_cpu, total_ram, total_storage, status) VALUES(?,?,?,?,?,?,?)",
        servers_data
    )

# ---------------- VM REQUESTS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS vm_requests (
    vm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vm_name TEXT,
    team_name TEXT,
    server_id INTEGER,
    ip_address TEXT,
    cpu_required INTEGER,
    ram_required INTEGER,
    storage_required INTEGER,
    purpose TEXT,
    approval_status TEXT,
    assign_date TEXT,
    duration_days INTEGER
)
""")

# ---------------- IP POOL TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS ip_pool (
    ip_address TEXT PRIMARY KEY,
    ip_status TEXT
)
""")

# ---------------- AUTH USERS TABLE ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS auth_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# Insert default admin user if empty
cur.execute("SELECT COUNT(*) FROM auth_users")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO auth_users (email, password) VALUES (?, ?)", ("itadmin@infraon.io", "admin1234"))

conn.commit()
conn.close()

print("✅ Database created successfully!")