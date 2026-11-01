from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from middlewares import middleware_methods
from tools import lc_tools

load_dotenv()

MODEL = "openai:gpt-5.4-mini"
# MODEL = "deepseek:deepseek-chat"

SYSTEM_PROMPT = """
You are a friendly clinic front-desk assistant. 
Keep answers short and clear. 
"""

# checkpointer loads the chat's messages before each call and saves them after
# diff types of checkpointers - InMemorySaver, SqliteSaver, PostgresSaver, Redis & MongoDB savers
# "The checkpointer decides where the chat is saved. InMemorySaver keeps it in memory,
# so when we stop the program, it's gone.
# Later save-resume video we'll swap in one that saves to a file, and nothing else in our code changes."
# and once we get to our clinic-assistant, we will use PostgresSaver so all the chats gets saved
# into our Postgres database
inmemory_checkpointer = InMemorySaver()
thread_id = "chat-101"
config = {"configurable": {"thread_id": thread_id}}

agent = create_agent(
    model=MODEL,
    system_prompt=SYSTEM_PROMPT,
    tools=lc_tools,
    middleware=middleware_methods,
    checkpointer=inmemory_checkpointer,
)
# print(f"[LOG] Chat started with {MODEL}, type quit to exit")

while True:
    user_prompt = input("You: ")

    if user_prompt == "quit":
        # print("[LOG] User typed quit, ending the chat")
        break

    # print("[LOG] Calling the agent with the user's question")
    result = agent.invoke({"messages": [HumanMessage(user_prompt)]}, config=config)

    messages = result["messages"]
    print("========== conv history =============")
    for message in messages:
        if message.type == "ai" and message.tool_calls:
            for tool_call in message.tool_calls:
                print(
                    f"[LOG] ai asks for a tool: {tool_call['name']} {tool_call['args']}"
                )
        else:
            print(f"[LOG] {message.type}: {message.content}")
    print("========== conv history =============")

    ai_response = messages[-1].content
    print("Bot:", ai_response)
