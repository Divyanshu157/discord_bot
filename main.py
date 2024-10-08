import os
from fastapi import FastAPI, Request, Header, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from utils.discord_api import register_commands
from commands.mom import handle_mom_command
from commands.hello import handle_hello_command
from commands.meet import handle_meet_command, handle_button_interaction   # Import the new meet command handler
import nacl.signing
import nacl.exceptions
from commands.mom_handler import create_table
from commands.detail import handle_detail_command, handle_logout_interaction 
from commands.database import create_user_logs_table , delete_user_logs_table

load_dotenv()

print("Start")

DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")  # Add this to .env

# app = FastAPI()
# print("Called register commands")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register commands when the app starts
    print("Called register commands")

    # create database at start of application
    create_table()
    delete_user_logs_table()
    create_user_logs_table() 
    await register_commands()
    yield

app = FastAPI(lifespan=lifespan) 

# Signature verification function
def verify_discord_signature(public_key: str, signature: str, timestamp: str, body: str) -> bool:
    
    try:
        public_key = nacl.signing.VerifyKey(bytes.fromhex(public_key))
        message = timestamp.encode() + body.encode()  # Combine timestamp and body
        public_key.verify(message, bytes.fromhex(signature))  # Verify signature
        return True
    except (nacl.exceptions.BadSignatureError, ValueError):
        return False

@app.post("/interactions")
async def interactions(
    request: Request,
    x_signature_ed25519: str = Header(...),
    x_signature_timestamp: str = Header(...)
):
    body = await request.body()

    # Verify the Discord signature
    if not verify_discord_signature(DISCORD_PUBLIC_KEY, x_signature_ed25519, x_signature_timestamp, body.decode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid request signature")

    data = await request.json()
    print("Incoming data:", data)

    # Respond to Discord's verification PING
    interaction_type = data.get("type")
    if interaction_type == 1:  # PING verification
        return {"type": 1}  # Respond with PONG

    # Handle Slash Commands (type 2: APPLICATION_COMMAND)
    if interaction_type == 2:
        command_name = data["data"].get("name")
        if command_name == "hello":
            # Call the function from hello.py
            return await handle_hello_command(data)
        elif command_name == "meet":
            # Call the function from meet.py
            return await handle_meet_command(data)
        elif command_name == "mom":

            # options = data["data"]["options"]
            # participants = options[0]["value"]  # Fetch participants from the user input
            # topic = options[1]["value"]         # Fetch topic from the user input
            # summary = options[2]["value"]       # Fetch summary from the user input

            # Pass the user input to the command handler
            return await handle_mom_command(data)
        elif command_name == "detail":  # Handle the `/detail` command
            return await handle_detail_command(data)
        

    
    if interaction_type == 3:
        print("Button interaction received:", data)
        custom_id = data["data"]["custom_id"]
        if custom_id.startswith("logout_"):  # Logout button click handling
            # Call the logout button handler
            return await handle_logout_interaction(data)
        # Existing button handler from meet.py
        return await handle_button_interaction(data)

    return {"error": "Unknown command or malformed request"}

# Simple test endpoints to verify the bot is running
@app.get("/")
async def root():

    return {"message": "Bot is running!"}

@app.get("/test")
async def test():
    return {"message": "This is a test endpoint!"}



# /*type: 1 (PING): Discord sends this to verify the interaction endpoint is working. The server responds with a PONG ({"type": 1}).
# type: 2 (APPLICATION_COMMAND): These are slash commands like /hello or /meet. This is when a user invokes a custom slash command.
# type: 3 (MESSAGE_COMPONENT): These interactions are triggered by user interaction with message components like buttons or select menus.
# type: 4 (MODAL_SUBMIT): Interactions related to modals (pop-up forms or input boxes).*/