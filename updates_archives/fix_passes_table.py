import sqlite3

# Connect to the database
conn = sqlite3.connect("data/app.db")
cursor = conn.cursor()

# Drop the old passes table if it exists
cursor.execute("DROP TABLE IF EXISTS passes")

# Create the new passes table with an id column
cursor.execute("""
    CREATE TABLE passes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER
    )
""")

# Save and close
conn.commit()
conn.close()

print("✅ Passes table fixed.")