from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from pydantic import BaseModel, Field

load_dotenv()


# the form the second LLM call fills in (structured output, like in the structured output video)
class InviteMessage(BaseModel):
    subject: str = Field(description="The subject of the email to the user's friends")
    greeting: str = Field(description="The greeting of the email to the user's friends")
    email_body: str = Field(description="The body of the email to the user's friends")
    cricket_joke: str = Field(
        description="A short cricket joke to include in the email"
    )


# the second call has its own prompt: no tools, and none of our conversation
invite_prompt = """
You write short emails to a group of friends.
You will be given a cricket ground booking confirmation message.
Fill in every field.
Include all the information from the booking confirmation in the email body.
The subject should be a short and catchy subject line.
The greeting should be a friendly greeting.
The cricket joke should be a short and funny joke about cricket.
The email body should be two or three lines telling them which ground, which day and what time to turn up, and the booking confirmation number.
Make sure to add a note in there to a friend named Ravi to show up on time as he is always late, with a funny sarcastic note.
"""

# MODEL = "openai:gpt-5.2"
MODEL = "deepseek:deepseek-chat"

invite_agent = create_agent(
    model=MODEL,
    system_prompt=invite_prompt,
    response_format=InviteMessage,
)


# Prompt chaining: a second, separate LLM call
# the only thing it gets is the booking confirmation from the first call
@tool(
    name_or_callable="draft_invite_message",
    description="Write a short invite message for the user's friends about a booking. Only call this once the user has said they want a message drafted.",
)
def draft_invite_message(booking_confirmation: str) -> dict:
    print("[TOOL] draft_invite_message() on DeepSeek")
    result = invite_agent.invoke({"messages": [HumanMessage(booking_confirmation)]})
    invite: InviteMessage = result["structured_response"]
    return invite.model_dump()
