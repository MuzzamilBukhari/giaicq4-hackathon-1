from datetime import datetime

async def log_message(session_id: str, sender: str, text: str):
    """
    Log a message to the database.
    """
    try:
        from db.models import create_message
        await create_message(session_id, sender, text)
    except Exception as e:
        print(f"Error logging message: {e}")
        raise