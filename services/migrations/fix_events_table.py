import sqlite3
import os

DB_PATH = os.path.join("data", "app.db")

def fix_events_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop old table if it exists
    cur.execute("DROP TABLE IF EXISTS events")

    # Create correct schema
    cur.execute("""
        CREATE TABLE events (
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
    print("✅ Events table recreated with correct schema.")

if __name__ == "__main__":
    fix_events_table()