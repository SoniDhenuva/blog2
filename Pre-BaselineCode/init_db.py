import sqlite3

# Connect to (or create) a database file
conn = sqlite3.connect("my_database.db")  

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "users" table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing unique ID
        name TEXT NOT NULL,  -- Name is required (cannot be NULL)
        age INTEGER  -- Age can be NULL
    )
""")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table initialized successfully.")
