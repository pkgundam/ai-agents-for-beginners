from typing import Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import BaseModel

load_dotenv()

MODEL = "openai:gpt-5.4-mini"
# MODEL = "deepseek:deepseek-chat"


class ClinicReply(BaseModel):
    summary: str
    intent: Literal["book_appointment", "ask_hours", "other"]
    next_question: str


SYSTEM_PROMPT = """
You are a friendly front-desk assistant for a clinic. 
Fill every field in the form. 
"""

agent = create_agent(
    model=MODEL, system_prompt=SYSTEM_PROMPT, response_format=ClinicReply
)
print(f"[LOG] Chat started with {MODEL}, type quit to exit")

while True:
    user_prompt = input("You: ")

    if user_prompt == "quit":
        print("[LOG] User typed quit, ending the chat")
        break

    print("[LOG] Calling the agent with the user's question")
    result = agent.invoke({"messages": [HumanMessage(user_prompt)]})

    reply = result["structured_response"]
    print("[LOG] Got back a filled ClinicReply:", reply)

    print("Intent:", reply.intent)
    if reply.intent == "book_appointment":
        print("App: start the booking")
    elif reply.intent == "ask_hours":
        print("App: share the clinic hours")
    else:
        print("App: pass it to the front desk")

    print("Bot:", reply.next_question)
