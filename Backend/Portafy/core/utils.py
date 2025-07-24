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
    """_summary_
    Connects to the Gemini API and returns the response
    Args:
        message (str): the message to send to the API

    Returns:
        str: the response from the API
    """
    try:
        import google.generativeai as genai
        from decouple import config

        genai.configure(api_key=config("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-1.5-flash-002")
        response = model.generate_content(message)
        return response.text if response.text else "No response from Gemini API"
    
    except Exception as e:
        return f"Error connecting to Gemini API: {str(e)}"