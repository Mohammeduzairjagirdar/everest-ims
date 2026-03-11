import sqlite3

conn = sqlite3.connect("infra.db")
cur = conn.cursor()

# ── servers table ──
cols = [row[1] for row in cur.execute("PRAGMA table_info(servers)").fetchall()]
print("servers columns:", cols)

if "server_id" not in cols:
    cur.execute("ALTER TABLE servers ADD COLUMN server_id INTEGER")
    cur.execute("UPDATE servers SET server_id = rowid")
    print("✅ Added server_id to servers (populated from rowid)")
else:
    print("✅ servers.server_id already exists")

# ── vm_requests table ──
cols_vm = [row[1] for row in cur.execute("PRAGMA table_info(vm_requests)").fetchall()]
print("vm_requests columns:", cols_vm)

if "server_id" not in cols_vm:
    cur.execute("ALTER TABLE vm_requests ADD COLUMN server_id INTEGER")
    print("✅ Added server_id to vm_requests")
else:
    print("✅ vm_requests.server_id already exists")

conn.commit()
conn.close()
print("\nDone! Now run:  streamlit run app.py")