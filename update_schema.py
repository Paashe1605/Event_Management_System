import sqlite3
conn = sqlite3.connect("event_management.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(events);")
print(cursor.fetchall())
conn.close()