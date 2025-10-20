# your_app/tasks.py

from google import genai
from decouple import config
from celery import shared_task


@shared_task
def gemini_api(history: list, new_message: str) -> dict:
    """
    Continues a chat session using the client.chats.create() method.
    The 'history' list should contain content objects for context.

    Example history format:
    [
      {"role": "user", "parts": [{"text": "Hello, I am a developer."}]},
      {"role": "model", "parts": [{"text": "That's cool! What are you building?"}]},
    ]
    """
    try:
        client = genai.Client()

        # Use the client.chats service and the create method for persistent conversation
        chat = client.chats.create(
            model="gemini-2.5-flash",
            history=history,  # Pass the prior conversation history
        )

        # Send the new message
        response = chat.send_message(new_message)

        # Return the updated history and the new reply
        return {
            "reply": response.text,
            "new_history": chat.get_history(),  # Retrieve the full, updated history
        }

    except Exception as e:
        return {"reply": f"Error: Chat failed. {e}", "new_history": history}
