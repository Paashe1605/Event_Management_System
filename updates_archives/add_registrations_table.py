import sqlite3

def add_registrations_table(db_path="data/app.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ Create registrations table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        event_id INTEGER NOT NULL,
        pass_id TEXT UNIQUE NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(event_id) REFERENCES events(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Registrations table added successfully.")

if __name__ == "__main__":
    add_registrations_table()