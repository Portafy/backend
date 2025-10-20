from google import genai
from decouple import config

def get_main_path(request) -> str:
    """_summary_
    Extracts the main path from the full path
    Args:
        request (_HttpRequest_): the request obj

    Returns:
        str: the main path
    """
    full_path = request.build_absolute_uri()
    relative_path = request.path

    return full_path.split(relative_path)[0]


def gemini_api(message: str) -> str:
    """
    Generates result content using the recommended gemini model.
    Uses the new google-genai SDK.
    """
    try:
        client = genai.Client(api_key=str(config("GEMINI_API_KEY")))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
        )
        
        return response.text if response.text else "No response from Gemini API"
    except Exception as e:
        return f"Error: Failed to generate content. {e}"