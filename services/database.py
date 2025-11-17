import sqlite3

def init_db():
    conn = sqlite3.connect("data/app.db")
    cursor = conn.cursor()

    # Create events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        venue TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        final_entry_time TEXT NOT NULL,
        end_time TEXT NOT NULL
    )
    """)

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        aadhar_number TEXT UNIQUE NOT NULL
    )
    """)

    # Create organizers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizers (
        organizer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Create passes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passes (
        pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER,
        qr_code TEXT,
        pdf_path TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(event_id) REFERENCES events(event_id)
    )
    """)

    conn.commit()
    conn.close()