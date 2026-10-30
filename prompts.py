from memory import load_user_facts, load_user_preferences, load_user_routines

# 1. Instructions: what the job is, which tool to use when, and the rules (no examples)
INSTRUCTIONS = """Answer the user's question clearly and briefly.
Use the tools when the user asks for live data:
- get_current_datetime for the current date or time.
- get_weather for the current weather in a city.
- get_stock_price for the latest price of a stock symbol.
- get_top_news for the latest news headlines.
Never invent live data. Use only the values a tool returns.
If you do not know something, say that you do not know."""

# 2. Role: who the assistant is
ROLE = """You are a calm and practical personal assistant.
You keep answers short, and you always end with one practical suggestion.
You are honest about what you do not know, and you never guess live data."""

# 3. Examples: they only show the shape of the answer, so we tell the LLM never to copy their values
EXAMPLE_RULES = """The examples below show only the answer format.
Always call the tool for live values. Never reuse an example value."""

WEATHER_EXAMPLE = """User: What is the weather in Sample City?
Assistant:
WEATHER: Sample City
68 F, light rain, humidity 70%
SUGGESTION: <<a sample suggestion about the weather>>"""

STOCK_EXAMPLE = """User: What is the price of DEMO?
Assistant:
STOCK: DEMO
123.45 USD
SUGGESTION: <<a sample suggestion about the stock>>"""

NEWS_EXAMPLE = """User: What is in the news?
Assistant:
NEWS:
- first headline
- second headline"""

MEMORY_RULES = """Memory rules:
- If the user shares a lasting fact (their name, where they live, where they work), use the remember tool with type fact.
- If the user shares a preference (the temperature unit they like, the stocks they follow), use the remember tool with type preference.
- Only save what is new. If it is already in user_facts or user_preferences, or you already saved it in this chat, don't save it again.
- Don't save one-off questions or greetings or anything that is not a lasting fact or preference.
- When you answer, use what we know about the user: "home" means where they live, "work" means where they work, "my stocks" means the stocks they follow.
- If the user asks for one of their routines, follow its steps in order in the routines mentioned."""


# zero-shot: instructions only, and zero examples
def zero_shot_prompt() -> str:
    return INSTRUCTIONS


# role: who it is, on top of the instructions (still zero examples, so still zero-shot)
def role_prompt() -> str:
    return ROLE + "\n\n" + INSTRUCTIONS


# one-shot: the role prompt, plus one example
def one_shot_prompt() -> str:
    return (
        ROLE + "\n\n" + INSTRUCTIONS + "\n\n" + EXAMPLE_RULES + "\n\n" + WEATHER_EXAMPLE
    )


# few-shot: the one-shot prompt, plus a few more examples
def few_shot_prompt() -> str:
    return (
        ROLE
        + "\n\n"
        + INSTRUCTIONS
        + "\n\n"
        + EXAMPLE_RULES
        + "\n\n"
        + WEATHER_EXAMPLE
        + "\n\n"
        + STOCK_EXAMPLE
        + "\n\n"
        + NEWS_EXAMPLE
    )


# we turn the saved facts or preferences into lines, like "home_city: Atlanta"
def json_to_text(saved: dict) -> str:
    if not saved:
        return "Nothing yet."
    lines = ""
    for key, value in saved.items():
        lines += f"{key}: {value}\n"
    return lines.strip()


# we take what's in the cabinet and put it on the desk, inside the system prompt
def build_system_prompt(prompt: str) -> str:
    return (
        prompt  ## this will be the 8 step cricket ground booking workflow for 09 ai agent video
        + "\n\n"
        + MEMORY_RULES
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
