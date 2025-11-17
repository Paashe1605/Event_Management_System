from db import get_connection, get_cursor, close_connection

conn = get_connection()
cursor = get_cursor(conn)

try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("✅ Added 'role' column with default 'user'.")
except Exception as e:
    print("⚠️ Could not add 'role':", e)

conn.commit()
close_connection(conn)