# In commands/mom.py

from commands.mom_handler import save_meeting_notes

async def handle_mom_command(data):
    options = {opt["name"]: opt["value"] for opt in data["data"]["options"]}

    participants = options.get("participants")
    topic = options.get("topic")
    summary = options.get("summary")

    # Save the meeting notes
    save_meeting_notes(participants, topic, summary)

    # Return the response back to Discord
    return {
        "type": 4,  # ACKNOWLEDGE_WITH_SOURCE (immediate response)
        "data": {
            "content": f"Meeting notes saved!\nParticipants: {participants}\nTopic: {topic}\nSummary: {summary}"
        }
    }
