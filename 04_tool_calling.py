from dotenv import load_dotenv
from openai import OpenAI

from llm_with_tools import ask_llm_with_tools

load_dotenv()
client = OpenAI()

system_prompt = """You are a helpful assistant. Keep your answers short.
If you need the current date or time, use the get_current_datetime tool.
If you need the weather in a city, use the get_weather tool.
If you need a stock price, use the get_stock_price tool.
If you need the latest news, use the get_top_news tool.
"""

# we need 4 tools
# 1. date time tool
# 2. weather tool
# 3. stock price tool
# 4. latest news tool

# the chat loop: keep asking questions until the user types "quit"
while True:
    question = input("USER: ")
    if question.strip().lower() == "quit":
        break

    # we start fresh for every question, so the LLM doesn't remember the earlier ones
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    answer = ask_llm_with_tools(messages)
    print("LLM:", answer)
    print()  # blank line between questions
