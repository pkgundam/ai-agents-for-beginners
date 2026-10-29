from dotenv import load_dotenv
from openai import OpenAI

from llm_with_tools import ask_llm_with_tools
from memory import rolling_summary

load_dotenv()
client = OpenAI()

system_prompt = """You are a helpful assistant. Keep your answers short.
If you need the current date or time, use the get_current_datetime tool.
If you need the weather in a city, use the get_weather tool.
If you need a stock price, use the get_stock_price tool.
If you need the latest news, use the get_top_news tool.
"""

messages = [{"role": "system", "content": system_prompt}]

# the chat loop: keep asking questions until the user types "quit"
while True:
    question = input("USER: ")
    if question.strip().lower() == "quit":
        break

    messages.append({"role": "user", "content": question})

    print("   --- messages going to the LLM ---")
    for message in messages[1:]:
        if message["role"] == "user":
            print("   User:", message["content"])
        else:
            print("   Assistant:", message["content"])

    answer = ask_llm_with_tools(messages)
    messages.append({"role": "assistant", "content": answer})

    messages = rolling_summary(
        messages
    )  # keep only the last 4 messages in short term memory

    print("LLM:", answer)
    print()  # blank line between questions
