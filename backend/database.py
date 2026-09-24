import sqlite3
from datetime import datetime
from backend.config import DB_PATH
from pathlib import Path


# ─── Connection ────────────────────────────────────────────────────────────────
def get_conn():
    print("DB_PATH:", DB_PATH)
    print("Resolved:", Path(DB_PATH).resolve())

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ─── Init tables ───────────────────────────────────────────────────────────────
def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp    TEXT NOT NULL,
            zone         TEXT NOT NULL,
            violation    TEXT NOT NULL,
            confidence   REAL NOT NULL,
            snapshot     TEXT,
            acknowledged INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL,
            role      TEXT DEFAULT 'supervisor',
            full_name TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Tables initialized")


# ─── Violations ────────────────────────────────────────────────────────────────
def log_violation(zone: str, violation: str, confidence: float, snapshot: str = None):
    conn = get_conn()
    conn.execute("""
        INSERT INTO violations (timestamp, zone, violation, confidence, snapshot, acknowledged)
        VALUES (?, ?, ?, ?, ?, 0)
    """, (datetime.now().isoformat(), zone, violation, confidence, snapshot))
    conn.commit()
    conn.close()


def get_violations(limit: int = 50, zone: str = None, violation: str = None):
    conn = get_conn()
    query = "SELECT * FROM violations WHERE 1=1"
    params = []

    if zone:
        query += " AND zone = ?"
        params.append(zone)
    if violation:
        query += " AND violation = ?"
        params.append(violation)

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_violations(since_id: int = 0):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM violations WHERE id > ? ORDER BY timestamp DESC",
        (since_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def acknowledge_violation(violation_id: int):
    conn = get_conn()
    conn.execute("UPDATE violations SET acknowledged = 1 WHERE id = ?", (violation_id,))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_conn()
    today = datetime.now().date().isoformat()

    total    = conn.execute("SELECT COUNT(*) FROM violations").fetchone()[0]
    unacked  = conn.execute("SELECT COUNT(*) FROM violations WHERE acknowledged = 0").fetchone()[0]
    hardhat  = conn.execute("SELECT COUNT(*) FROM violations WHERE violation = 'No Hardhat'").fetchone()[0]
    vest     = conn.execute("SELECT COUNT(*) FROM violations WHERE violation = 'No Safety Vest'").fetchone()[0]
    today_ct = conn.execute("SELECT COUNT(*) FROM violations WHERE DATE(timestamp) = ?", (today,)).fetchone()[0]

    by_zone = conn.execute(
        "SELECT zone, COUNT(*) as count FROM violations GROUP BY zone"
    ).fetchall()

    hourly = conn.execute("""
        SELECT strftime('%H:00', timestamp) as hour, COUNT(*) as count
        FROM violations WHERE DATE(timestamp) = ?
        GROUP BY hour ORDER BY hour
    """, (today,)).fetchall()

    conn.close()
    return {
        "total": total,
        "unacknowledged": unacked,
        "no_hardhat": hardhat,
        "no_vest": vest,
        "today": today_ct,
        "by_zone": [dict(r) for r in by_zone],
        "hourly":  [dict(r) for r in hourly]
    }


def get_zones():
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT zone FROM violations").fetchall()
    conn.close()
    return [r[0] for r in rows]


def clear_violations():
    conn = get_conn()
    conn.execute("DELETE FROM violations")
    conn.commit()
    conn.close()


# ─── Users ─────────────────────────────────────────────────────────────────────
def get_user(username: str, password_hash: str):
    conn = get_conn()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password_hash)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def seed_users(users: list):
    conn = get_conn()
    for u in users:
        try:
            conn.execute(
                "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                u
            )
            print(f"[DB] Seeded user: {u[0]}")
        except sqlite3.IntegrityError:
            print(f"[DB] User exists: {u[0]}")
    conn.commit()
    conn.close()



