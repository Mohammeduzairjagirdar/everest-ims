import sqlite3
import pandas as pd

# connect DB
conn = sqlite3.connect("infra.db")
cursor = conn.cursor()

print("Connected to database")

# ---------------- LOAD SERVERS ----------------
try:
    servers_df = pd.read_csv("data/servers.csv")
    servers_df.to_sql("servers", conn, if_exists="append", index=False)
    print("Servers data inserted successfully")
except Exception as e:
    print("Servers insert error:", e)

# ---------------- LOAD IP POOL ----------------
try:
    ip_df = pd.read_csv("data/ip_pool.csv")
    ip_df.to_sql("ip_pool", conn, if_exists="append", index=False)
    print("IP Pool data inserted successfully")
except Exception as e:
    print("IP Pool insert error:", e)

conn.commit()
conn.close()

print("Database population completed")
