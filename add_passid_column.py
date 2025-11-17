import sqlite3
from db import get_connection, get_cursor, close_connection

try:
    conn = get_connection()
    cursor = get_cursor(conn)

    # Add pass_id column if it doesn't already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]

    if "pass_id" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN pass_id TEXT")
        conn.commit()
        print("✅ Column 'pass_id' added successfully.")
    else:
        print("ℹ️ Column 'pass_id' already exists, no changes made.")

    close_connection(conn)

except Exception as e:
    print(f"Error: {e}")