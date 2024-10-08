from datetime import datetime, timezone
import sqlite3
from dateutil import parser

# Database setup (assuming db.sqlite3 is your SQLite database)
def store_login_details(user_id, name, roll_no, login_time):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_logs (user_id, name, roll_no, login_time) VALUES (?, ?, ?, ?)",
        (user_id, name, roll_no, login_time)
    )
    conn.commit()
    conn.close()

def update_logout_time(user_id, logout_time):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_logs SET logout_time = ? WHERE user_id = ? AND logout_time IS NULL",
        (logout_time, user_id)
    )
    conn.commit()
    conn.close()

def calculate_time_interval(login_time, logout_time):
    """Calculate the time interval between login and logout."""
    return logout_time - login_time

def format_time_interval(time_interval):
    """Format timedelta to hh:mm:ss."""
    total_seconds = int(time_interval.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Handle the `/detail` command
async def handle_detail_command(data):
    """Handles the detail command for logging in a user."""
    user_id = data["member"]["user"]["id"]
    name = data["data"]["options"][0]["value"]  # Assuming the name is passed as an option
    roll_no = data["data"]["options"][1]["value"]  # Assuming roll_no is the second option
    login_time = datetime.now(timezone.utc)  # Get timezone-aware current UTC time

    # Store login details in the database
    store_login_details(user_id, name, roll_no, login_time)

    # Create a response with a button for logging out
    return {
        "type": 4,  # Interactive response
        "data": {
            "content": f"Welcome {name}! Your login has been recorded.",
            "components": [
                {
                    "type": 1,  # Action row
                    "components": [
                        {
                            "type": 2,  # Button
                            "style": 1,  # Primary button
                            "label": "Logout",
                            "custom_id": f"logout_{user_id}_{name}"  # Include name in custom_id for later use
                        }
                    ]
                }
            ]
        }
    }

# Handle the logout button interaction
async def handle_logout_interaction(data):
    """Handles the logout interaction for a user."""
    user_id = data["member"]["user"]["id"]
    logout_time = datetime.now(timezone.utc)  # Get timezone-aware current UTC time

    # Update the logout time in the database
    update_logout_time(user_id, logout_time)

    # Fetch the corresponding login time (for calculating interval)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT login_time, name FROM user_logs WHERE user_id = ? AND logout_time IS NOT NULL", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        # Use dateutil.parser to handle the datetime parsing
        login_time, name = row
        login_time = parser.isoparse(login_time)

        time_interval = calculate_time_interval(login_time, logout_time)

        # Format the time interval to hh:mm:ss
        formatted_interval = format_time_interval(time_interval)

        # Send a message with the entered name and formatted time interval
        return {
            "type": 4,  # Interactive response
            "data": {
                "content": f"{name} was logged in for {formatted_interval}.",  # Use the captured name
            }
        }

    return {"error": "Logout time could not be recorded."}
