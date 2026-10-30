from dotenv import load_dotenv
from openai import OpenAI

from storage import (
    load_facts,
    load_preferences,
    load_routines,
    store_chat_summary,
    store_facts,
    store_preferences,
)

load_dotenv()
client = OpenAI()

WINDOW = 40  # the number of messages to keep in short term memory

# rolling summary: once the conversation reaches 10 messages, we summarize the older ones
SUMMARIZE_AT = 100

# The system prompt for the summary: what to keep, what to drop, and how short it should be
summary_prompt = """You summarize a conversation between a user and an assistant, so the assistant can continue it later.

You may get an earlier summary at the top. Merge it with the new messages into ONE new summary.

Keep:
- Facts about the user: their name, where they live, what they like or prefer.
- What the user asked for, and the important answers (cities, stocks, dates, numbers).
- Anything the user asked to remember, or a question that is still not answered.

Drop:
- Greetings, small talk and thank-yous.
- Details nobody will need again.

Rules:
- Weather, stock prices and news change quickly, so say they were from earlier in the chat.
- Only write what is in the messages. Never make anything up.
- Write short bullet points, at most 8, in plain English."""


# Sliding window: the system prompt stays, and only the last 4 messages of the conversation stay with it
def sliding_window(messages):
    # the system prompt is always the first message, and it always stays
    system_prompt = messages[0]
    conversation = messages[1:]

    # the oldest messages fall off the desk
    # keep only last 4 messages of the conversation, plus the system prompt
    return [system_prompt] + conversation[-WINDOW:]


# Rolling summary: the conversation grows until it reaches 10 messages,
# then we squeeze the older ones into a summary and keep the last 4
def rolling_summary(messages):
    system_prompt = messages[0]
    conversation = messages[1:]

    # the conversation is still small, so we don't summarize yet
    if len(conversation) < SUMMARIZE_AT:
        return messages

    # everything except the last 4 messages falls off the desk, for example the first 6 of 10
    # (after the first time, this includes the old summary, so it gets folded into the new one)
    old_messages = conversation[:-WINDOW]
    summary = summarize(old_messages)

    # the summary goes right after the system prompt, then the last 4 messages
    summary_message = {
        "role": "system",
        "content": f"Summary of the earlier conversation: {summary}",
    }
    return [system_prompt, summary_message] + conversation[-WINDOW:]


def summarize(old_messages):
    print("=========== summarizing the old messages ===========")
    # we turn the old messages into plain text, one line per message, like "user: What's the weather in Atlanta?"
    old_chat = ""
    for message in old_messages:
        if "role" not in message:
            continue
        old_chat += f"{message['role']}: {message['content']}\n"

    # we send the old messages, and the LLM writes one short summary
    messages = [
        {"role": "system", "content": summary_prompt},
        {"role": "user", "content": old_chat},
    ]
    response = client.responses.create(model="gpt-5.2", input=messages)
    return response.output_text


# Long-term memory methods: we save and load facts, preferences and routines, so we can use them in future chats
# we maintain anything to do with memory in this file.


# store user facts
def store_fact(key: str, value: str) -> dict:
    return store_facts(key, value)


# store user preferences
def store_preference(key: str, value: str) -> dict:
    return store_preferences(key, value)


# load user facts
def load_user_facts() -> dict:
    return load_facts()


# load user preferences
def load_user_preferences() -> dict:
    return load_preferences()


# load user routines
def load_user_routines() -> str:
    return load_routines()


# when the chat ends, we summarize it and save the summary
# (we reuse the same summarize from above, because it already keeps what matters about the user)
def store_chat(messages: list[dict]) -> None:
    # everything except the system prompt
    conversation = messages[1:]

    # nothing was said, so there is nothing to save
    if not conversation:
        return

    summary = summarize(conversation)
    store_chat_summary(summary)
