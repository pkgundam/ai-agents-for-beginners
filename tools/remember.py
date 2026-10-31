from typing import Literal

from langchain.tools import tool

from memory import store_fact, store_preference


# we save one fact or preference about the user, so we still know it in future chats
@tool(
    name_or_callable="remember",
    description="Save a lasting fact or preference about the user, so we still know it in future chats. Use the same key again to update it.",
)
def remember(type: Literal["fact", "preference"], key: str, value: str) -> dict:
    if type not in ["fact", "preference"]:
        return {"error": f"Invalid type: {type}. Must be 'fact' or 'preference'."}

    if type == "preference":
        return store_preference(key, value)
    return store_fact(key, value)
