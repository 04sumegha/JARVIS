import functools

from services.keyboard import decrease_brightness, increase_brightness

tools = [
    {
        "type": "function",
        "function": {
            "name": "increase_brightness",
            "description": "Increase laptop screen brightness",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "Amount to increase brightness (1-100). Set to 10 by default if not provided."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "decrease_brightness",
            "description": "Decrease laptop screen brightness",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "Amount to decrease brightness (1-100). Set to 10 by default if not provided."
                    }
                },
                "required": []
            }
        }
    }
]

names_to_functions = {
    "increase_brightness": functools.partial(increase_brightness),
    "decrease_brightness": functools.partial(decrease_brightness),
}
