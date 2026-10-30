from dotenv import load_dotenv
from openai import OpenAI

from llm_with_tools import ask_llm_with_tools
from memory import rolling_summary, store_chat
from prompts import build_system_prompt

load_dotenv()
client = OpenAI()

# when the chat starts, we load everything we saved in earlier chats, once
full_system_prompt = build_system_prompt()
print("   --- full system prompt ---")
print(full_system_prompt)
print("  --- end of full system prompt ---")

messages = [{"role": "system", "content": full_system_prompt}]

# the chat loop: keep asking questions until the user types "quit"
while True:
    question = input("USER: ")
    if question.strip().lower() == "quit":
        ## we need to summarize the chat and save it, so we can use it in future chats
        store_chat(messages)
        print("Saved this chat summary, so we can use it in future chats.")
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
