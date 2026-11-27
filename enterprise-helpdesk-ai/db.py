"""SQLite persistence for tickets."""
import os
import sqlite3

DB_PATH = os.environ.get("HELPDESK_DB", "helpdesk.db")

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, body TEXT,
            dept TEXT, priority TEXT, confidence REAL, sla_hours INTEGER,
            suggestion TEXT, status TEXT DEFAULT 'open',
            created TEXT DEFAULT CURRENT_TIMESTAMP)""")

def add(subject, body, dept, priority, confidence, sla_hours, suggestion):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO tickets (subject, body, dept, priority, confidence, sla_hours, suggestion)"
            " VALUES (?,?,?,?,?,?,?)",
            (subject, body, dept, priority, confidence, sla_hours, suggestion))
        return cur.lastrowid

def get_all(status=None):
    with conn() as c:
        q = "SELECT * FROM tickets" + (" WHERE status=?" if status else "")
        q += " ORDER BY CASE priority WHEN 'HIGH' THEN 0 WHEN 'MEDIUM' THEN 1 ELSE 2 END, id DESC"
        return [dict(r) for r in c.execute(q, (status,) if status else ())]

def resolve(ticket_id):
    with conn() as c:
        return c.execute("UPDATE tickets SET status='resolved' WHERE id=?", (ticket_id,)).rowcount

def stats():
    with conn() as c:
        by = lambda col: {r[0]: r[1] for r in c.execute(
            f"SELECT {col}, COUNT(*) FROM tickets WHERE status='open' GROUP BY {col}")}
        total = c.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        return {"total": total, "open_by_dept": by("dept"), "open_by_priority": by("priority")}
