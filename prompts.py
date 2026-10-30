from memory import load_user_facts, load_user_preferences, load_user_routines

system_prompt = """You are a helpful assistant. Keep your answers short.
If you need the current date or time, use the get_current_datetime tool.
If you need the weather in a city, use the get_weather tool.
If you need a stock price, use the get_stock_price tool.
If you need the latest news, use the get_top_news tool.

Memory rules:
- If the user shares a lasting fact (their name, where they live, where they work), use the remember tool with type fact.
- If the user shares a preference (the temperature unit they like, the stocks they follow), use the remember tool with type preference.
- Only save what is new. If it is already in user_facts or user_preferences, or you already saved it in this chat, don't save it again.
- Don't save one-off questions or greetings or anything that is not a lasting fact or preference.
- When you answer, use what we know about the user: "home" means where they live, "work" means where they work, "my stocks" means the stocks they follow.
- If the user asks for one of their routines, follow its steps in order in the routines mentioned.
"""


# we turn the saved facts or preferences into lines, like "home_city: Atlanta"
def json_to_text(saved: dict) -> str:
    if not saved:
        return "Nothing yet."
    lines = ""
    for key, value in saved.items():
        lines += f"{key}: {value}\n"
    return lines.strip()


# we take what's in the cabinet and put it on the desk, inside the system prompt
def build_system_prompt() -> str:
    return (
        system_prompt
        + f"""
<user_facts>
{json_to_text(load_user_facts())}
</user_facts>

<user_preferences>
{json_to_text(load_user_preferences())}
</user_preferences>

<routines>
{load_user_routines().strip()}
</routines>
"""
    )
