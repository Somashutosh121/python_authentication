import sqlite3

def create_users_table():
    """Creates the users table if it doesn't exist"""
    conn = sqlite3.connect("users.db")  # Connect to SQLite
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    
    conn.commit()  # Save changes
    conn.close()   # Close connection

# Run the function to create the table
create_users_table()
print("✅ Users table created successfully!")
