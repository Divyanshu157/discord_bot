import sqlite3

def create_user_logs_table():
    conn = sqlite3.connect('db.sqlite3')  # Use your actual database file
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT,
            roll_no TEXT,
            login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            logout_time DATETIME  
        )
    ''')
    conn.commit()
    conn.close()



def delete_user_logs_table():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user_logs;')
    conn.commit()
    conn.close()

