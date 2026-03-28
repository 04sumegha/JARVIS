import functools

from services.keyboard import adjust_system_level, mute_volume, take_screenshot, unmute_volume

tools = [
    {
        "type": "function",
        "function": {
            "name": "adjust_system_level",
            "description": "Adjust or query system brightness or volume based on the user request",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "enum": ["brightness", "volume"],
                        "description": "Which system control to adjust."
                    },
                    "action": {
                        "type": "string",
                        "enum": ["adjust", "query"],
                        "description": "Set to query to return the current value, or adjust to change it."
                    },
                    "direction": {
                        "type": "string",
                        "enum": ["increase", "decrease"],
                        "description": "Whether to increase or decrease."
                    },
                    "amount": {
                        "type": "integer",
                        "description": "Amount to adjust. Defaults to 10 for brightness and 5 for volume if not provided."
                    }
                },
                "required": ["target"]
            }
        }
    },
    {
    "type": "function",
        "function": {
            "name": "mute_volume",
            "description": "Mute system volume",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unmute_volume",
            "description": "Unmute system volume",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Take a screenshot and save it to a folder with an optional name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the screenshot file. Populate this only if user provides a name to the screenshot."
                    }
                },
                "required": []
            }
        }
    }
]

names_to_functions = {
    "adjust_system_level": functools.partial(adjust_system_level),
    "mute_volume": functools.partial(mute_volume),
    "unmute_volume": functools.partial(unmute_volume),
    "take_screenshot": functools.partial(take_screenshot)
}
