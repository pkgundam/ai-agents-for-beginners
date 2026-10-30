from typing import Literal

from memory import store_fact, store_preference


# we save one fact or preference about the user, so we still know it in future chats
def remember(type: Literal["fact", "preference"], key: str, value: str) -> dict:
    if type not in ["fact", "preference"]:
        return {"error": f"Invalid type: {type}. Must be 'fact' or 'preference'."}

    if type == "preference":
        return store_preference(key, value)
    return store_fact(key, value)


# What the LLM sees: a name, a description and the inputs
# schema
REMEMBER_TOOL = {
    "type": "function",
    "name": "remember",
    "description": "Save a lasting fact or preference about the user, so we still know it in future chats. Use the same key again to update it.",
    "parameters": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["fact", "preference"],
                "description": "fact: something true about the user, like their name, where they live or where they work. preference: something the user likes, like the temperature unit or the stocks they follow.",
            },
            "key": {
                "type": "string",
                "description": "A short snake_case name, for example name, home_city, work_city, temperature_unit or stocks. If it is already saved, use the same key.",
            },
            "value": {
                "type": "string",
                "description": "The fact or preference itself, for example Atlanta, Fahrenheit, or Apple and Tesla",
            },
        },
        "required": ["type", "key", "value"],
    },
}
