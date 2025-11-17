import sqlite3

conn = sqlite3.connect("data/app.db")
cursor = conn.cursor()

tables = ["users", "events", "passes", "registrations"]

for table in tables:
    print(f"\n🔍 Checking table: {table}")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        print(f" - {col[1]} ({col[2]})")

conn.close()