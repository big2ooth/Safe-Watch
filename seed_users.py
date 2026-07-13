import sqlite3
import hashlib
from backend.config import DB_PATH

def hash_password(p): 
    return hashlib.sha256(p.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT DEFAULT 'supervisor', full_name TEXT)")
users = [
    ("admin",      hash_password("admin123"),   "admin",      "Admin User"),
    ("supervisor", hash_password("ongc2026"),   "supervisor", "Site Supervisor"),
]
for u in users:
    try:
        conn.execute("INSERT INTO users (username, password, role, full_name) VALUES (?,?,?,?)", u)
        print(f"Created: {u[0]}")
    except:
        print(f"Exists: {u[0]}")
conn.commit()
conn.close()