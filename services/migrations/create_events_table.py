import sqlite3
import os

DB_PATH = os.path.join("data", "app.db")

def create_events_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            logo_path TEXT,
            status TEXT NOT NULL DEFAULT 'open'
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Events table ensured.")

if __name__ == "__main__":
    create_events_table()