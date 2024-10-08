# In commands/mom_handler.py

import sqlite3

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect('db.sqlite3')  # This will create 'db.sqlite3' in your project folder
    return conn

# Create the table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()


    


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meeting_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participants TEXT NOT NULL,
            topic TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Save meeting notes to the database
def save_meeting_notes(participants, topic, summary):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO meeting_notes (participants, topic, summary) 
        VALUES (?, ?, ?)
    ''', (participants, topic, summary))
    conn.commit()
    cursor.close()
    conn.close()
    print("Meeting notes saved successfully.")

