from datetime import datetime, timezone
import sqlite3

class UserLog:
    def __init__(self, user_id, name, roll_no, login_time, logout_time=None):
        self.user_id = user_id
        self.name = name
        self.roll_no = roll_no
        self.login_time = login_time
        self.logout_time = logout_time

    @staticmethod
    def store_login(user_id, name, roll_no):
        login_time = datetime.now(timezone.utc).isoformat()  # Store in ISO 8601 format

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_logs (user_id, name, roll_no, login_time) VALUES (?, ?, ?, ?)",
            (user_id, name, roll_no, login_time)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_logout(user_id):
        logout_time = datetime.now(timezone.utc).isoformat()  # Get current UTC time in ISO format

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_logs SET logout_time = ? WHERE user_id = ? AND logout_time IS NULL",
            (logout_time, user_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_login_time(user_id):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT login_time FROM user_logs WHERE user_id = ? AND logout_time IS NULL", 
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            # Parse the stored ISO 8601 string back to a datetime object
            return datetime.fromisoformat(row[0]).replace(tzinfo=timezone.utc)
        return None
