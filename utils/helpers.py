def format_response(function_name: str, result_value) -> str:
    """Format a natural language response based on the function executed and its result."""

    print(function_name, result_value)

    if function_name == "increase_brightness":
        return f"Brightness has been increased to {result_value}"
    elif function_name == "decrease_brightness":
        return f"Brightness has been decreased to {result_value}"
    else:
        return f"Action completed: {result_value}"