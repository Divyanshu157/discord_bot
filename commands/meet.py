
from commands.zoom import create_zoom_meeting
from commands.g import create_google_meet

async def handle_meet_command(data):
    # Respond with a message that has buttons for Zoom or Google Meet
    return {
        "type": 4,  # Type 4 is an interaction response
        "data": {
            "content": "Please choose between Zoom or Google Meet:",
            "components": [
                {
                    "type": 1,  # ActionRow type
                    "components": [
                        {
                            "type": 2,  # Button type
                            "label": "Zoom",
                            "style": 1,  # Primary (blue) button
                            "custom_id": "meet_zoom"
                        },
                        {
                            "type": 2,  # Button type
                            "label": "Google Meet",
                            "style": 1,  # Primary (blue) button
                            "custom_id": "meet_google_meet"
                        }
                    ]
                }
            ]
        }
    }

# Handle button interaction after user clicks
async def handle_button_interaction(interaction):
    print("Interaction data:", interaction)
    
    custom_id = interaction['data']['custom_id']  # Access the custom ID

    if custom_id == "meet_zoom":
        return await ask_for_meeting_details(interaction, "Zoom")
    elif custom_id == "meet_google_meet":
        return await ask_for_meeting_details(interaction, "Google_Meet")

# Ask for participant details and time
async def ask_for_meeting_details(interaction, platform):
    if platform == "Zoom":
        # Collect participant emails and time
        participants = ["participant1@example.com", "participant2@example.com"]
        meeting_time = '2024-09-23T10:00:00Z'  # Replace with user-provided time in UTC

        # Generate Zoom meeting link
        zoom_link = create_google_meet(participants, meeting_time)

        # Send response back to the user
        return {
            "type": 4,
            "data": {
                "content": f"Your {platform} meeting link: {zoom_link}",
            }
        }

    if platform == "Google_Meet":
        # Collect participant emails and time
        participants = ["participant1@example.com", "participant2@example.com"]
        meeting_time = '2024-09-23T10:00:00Z'  # Replace with user-provided time in UTC

        # Generate Zoom meeting link
        zoom_link = create_zoom_meeting(participants, meeting_time)

        # Send response back to the user
        return {
            "type": 4,
            "data": {
                "content": f"Your {platform} meeting link: {zoom_link}",
            }
        }
    
    

