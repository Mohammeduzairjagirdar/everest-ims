import sqlite3
import pandas as pd
import os

DB_NAME = "infra.db"

# check if database already exists
db_exists = os.path.exists(DB_NAME)

conn = sqlite3.connect(DB_NAME)

# ONLY run when database is new
if not db_exists:
    print("First time setup: Loading CSV data...")

    servers = pd.read_csv("servers.csv")
    ip_pool = pd.read_csv("ip_pool.csv")

    servers.to_sql("servers", conn, index=False)
    ip_pool.to_sql("ip_pool", conn, index=False)

    print("Database created and CSV data inserted.")

else:
    print("Database already exists. Nothing changed.")

conn.close()
