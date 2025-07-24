# your_app/tasks.py

import google.generativeai as genai
from decouple import config
from celery import shared_task

@shared_task
def gemini_api(message: str) -> str:
    """
        Connects to the Gemini API and returns the response
        Args:
            message (str): the message to send to the API

        Returns:
            str: the response from the API
    """
    try:
        genai.configure(api_key=config("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-pro") # or "gemini-1.5-flash"
        response = model.generate_content(message)
        return response.text if response.text else "No response from Gemini"
    except Exception as e:
        return f"Error: {str(e)}"




