from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage

load_dotenv()

MODEL = "openai:gpt-5.4-mini"
# MODEL = "deepseek:deepseek-chat"

SYSTEM_PROMPT = "You are a friendly teacher. Explain things so a 10-year-old can understand, in one short sentence."

agent = create_agent(model=MODEL, system_prompt=SYSTEM_PROMPT)
print(f"[LOG] Chat started with {MODEL}, type quit to exit")

while True:
    user_prompt = input("You: ")

    if user_prompt == "quit":
        print("[LOG] User typed quit, ending the chat")
        break

    print("[LOG] Calling the agent with the user's question")
    result = agent.invoke({"messages": [HumanMessage(user_prompt)]})
    for message in result["messages"]:
        print(f"[LOG] [RESPONSE] {message.type}: {message.content}")
        print("===========")

    ai_response = result["messages"][-1].content
    print("Bot:", ai_response)
