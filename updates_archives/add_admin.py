from db import get_connection, get_cursor, close_connection

conn = get_connection()
cursor = get_cursor(conn)

# Insert admin account with dummy values for required fields
cursor.execute("""
    INSERT INTO users (name, age, gender, address, phone, email, password, aadhar_number, event, role)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Admin User", 
    30,                 # age
    "Other",            # gender
    "Admin Address",    # address
    "9999999999",       # phone
    "admin@example.com",# email
    "admin123",         # password
    "000000000000",     # dummy aadhar
    "AdminEvent",       # dummy event
    "admin"             # role
))

conn.commit()
close_connection(conn)

print("✅ Admin user added successfully.")