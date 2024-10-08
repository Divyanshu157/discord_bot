import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")

print("In discord api")

async def register_commands():
    
    print("In register commands")
    base_url = f"https://discord.com/api/v10/applications/{DISCORD_APPLICATION_ID}/guilds/{DISCORD_GUILD_ID}/commands"
    
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # Fetch existing commands
        async with session.get(base_url, headers=headers) as response:
            existing_commands = await response.json()
            print(existing_commands)
            if response.status != 200:
                print(f"Error fetching commands: {existing_commands}")
                return

            # Check if commands already exist
            hello_exists = any(command["name"] == "hello" for command in existing_commands)
            meet_exists = any(command["name"] == "meet" for command in existing_commands)
            mom_exits = any(command["name"] == "mom" for command in existing_commands)
            detail_exists = any(command["name"] == "detail" for command in existing_commands)



            # Define the commands to register
            hello_command_data = {
                "name": "hello",
                "description": "Replies with hello!",
                "type": 1  # Slash command type
            }

            meet_command_data = {
                "name": "meet",
                "description": "Choose between Zoom and Google Meet",
                "type": 1  # Slash command type
            }
            mom_command = {
            "name": "mom",
            "description": "Record meeting notes",
            "options": [
            {
                "name": "participants",
                "description": "Enter participants (comma separated emails)",
                "type": 3,  # STRING type
                "required": True
            },
            {
                "name": "topic",
                "description": "Enter the topic of the meeting",
                "type": 3,  # STRING type
                "required": True
            },
            {
                "name": "summary",
                "description": "Enter a summary of the meeting",
                "type": 3,  # STRING type
                "required": True
            }
                ]
            }

            detail_command_data = {
                "name": "detail",
                "description": "Store user name, ID, roll number/employee ID, and login time",
                "type": 1,  # Slash command type
                "options": [
                    {
                        "name": "name",
                        "description": "Enter your name",
                        "type": 3,  # STRING type
                        "required": True
                    },
                    {
                        "name": "user_id",
                        "description": "Enter your ID",
                        "type": 3,  # STRING type
                        "required": True
                    },
                    {
                        "name": "roll_no_or_employee_id",
                        "description": "Enter your roll number or employee ID",
                        "type": 3,  # STRING type
                        "required": True
                    }
                ]
            }



            # Register the /hello command if not already registered
            if not hello_exists:
                async with session.post(base_url, headers=headers, json=hello_command_data) as post_response:
                    if post_response.status == 201:
                        print("'/hello' command registered successfully!")
                    else:
                        error_data = await post_response.json()
                        print(f"Failed to register '/hello' command: {error_data}")
            else:
                print("'/hello' command is already registered.")

            # Register the /meet command if not already registered
            if not meet_exists:
                async with session.post(base_url, headers=headers, json=meet_command_data) as post_response:
                    if post_response.status == 201:
                        print("'/meet' command registered successfully!")
                    else:
                        error_data = await post_response.json()
                        print(f"Failed to register '/meet' command: {error_data}")
            else:
                print("'/meet' command is already registered.")

            if  not mom_exits:

                async with session.post(base_url,headers=headers,json=mom_command) as post_response:
                    if post_response.status ==201:
                        print(" '/mom' command registered successfully")
                    else:
                        error_data=await post_response.json()
                        print(f"Failed to register '/mom' command: {error_data}")
            else:
                print("'/mom' command already registered")

            
            if not detail_exists:
                async with session.post(base_url, headers=headers, json=detail_command_data) as post_response:
                    if post_response.status == 201:
                        print("'/detail' command registered successfully!")
                    else:
                        error_data = await post_response.json()
                        print(f"Failed to register '/detail' command: {error_data}")
            else:
                print("'/detail' command is already registered.")




