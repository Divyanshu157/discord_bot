async def handle_hello_command(data):
    return {
        "type": 4,  # Respond immediately to the user
        "data": {
            "content": "Hello from FastAPI! Yes Hello"
        }
    }


print("in hello")