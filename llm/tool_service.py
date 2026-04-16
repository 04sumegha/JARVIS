import functools

from services.app import open_app, close_app
from services.keyboard import adjust_mute_volume, adjust_system_level, take_screenshot

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
            "name": "adjust_mute_volume",
            "description": "Mute or unmute system volume based on the user request",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["mute", "unmute"],
                        "description": "Whether to mute or unmute the system volume."
                    }
                },
                "required": ["action"]
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
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application using the Windows 'start' command. The app_name must be a valid executable name or system-recognized command (e.g., 'chrome', 'code', 'notepad', 'explorer', 'shell:Downloads'). Avoid vague names like 'vs code' or 'file explorer'.",
            "parameters": {
                "type": "object",
                "properties": {
                "app_name": {
                    "type": "string",
                    "description": "A valid Windows command or executable name that works with 'start'. Examples: 'chrome', 'code', 'notepad', 'explorer', 'shell:Downloads'"
                }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_app",
            "description": "Close an application using the Windows 'taskkill' command. The app_name must be a valid executable name (e.g., 'chrome.exe', 'notepad.exe'). If the user provides a common name like 'chrome', append '.exe' automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The executable name of the application to close (e.g., 'chrome.exe', 'notepad.exe', 'code.exe')."
                    }
                },
                "required": ["app_name"]
            }
        }
    }
]

names_to_functions = {
    "adjust_system_level": functools.partial(adjust_system_level),
    "adjust_mute_volume": functools.partial(adjust_mute_volume),
    "take_screenshot": functools.partial(take_screenshot),
    "open_app": functools.partial(open_app),
    "close_app": functools.partial(close_app)
}
