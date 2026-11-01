from langchain.agents.middleware import SummarizationMiddleware

MODEL = "openai:gpt-5.2"

SUMMARY_PROMPT = """
You summarize a conversation between a user and an assistant, so the assistant can continue it later.

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
- Write short bullet points, at most 8, in plain English.

Here is the list of messages so summarize:
{messages}
"""

# we want to trigger summary at 80% of context window
# and we want to keep 20% of the latest messages in short term memory, so we can continue the conversation
## if context window is lets say 100 messages (some xxxx tokens). Opus 5.5 is 1M tokens
# compaction/summary triggers at 81st message and 0-80th messages are summarized
# and 81-100th messages are kept in short term memory, so we can continue the conversation
summarize_old_messages = SummarizationMiddleware(
    model=MODEL,
    trigger=("fraction", 0.8),
    keep=("fraction", 0.2),
    summary_prompt=SUMMARY_PROMPT,
)
