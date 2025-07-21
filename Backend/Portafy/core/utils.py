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