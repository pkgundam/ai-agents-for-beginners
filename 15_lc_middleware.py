from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from middlewares import middleware_methods
from tools import lc_tools

load_dotenv()

MODEL = "openai:gpt-5.4-mini"
# MODEL = "deepseek:deepseek-chat"

SYSTEM_PROMPT = """
You are a friendly clinic front-desk assistant. 
Keep answers short and clear. 
"""

agent = create_agent(
    model=MODEL,
    system_prompt=SYSTEM_PROMPT,
    tools=lc_tools,
    middleware=middleware_methods,
)
# print(f"[LOG] Chat started with {MODEL}, type quit to exit")

while True:
    user_prompt = input("You: ")

    if user_prompt == "quit":
        # print("[LOG] User typed quit, ending the chat")
        break

    # print("[LOG] Calling the agent with the user's question")
    result = agent.invoke({"messages": [HumanMessage(user_prompt)]})

    ai_response = result["messages"][-1].content
    print("Bot:", ai_response)
