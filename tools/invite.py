from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI()


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


# Prompt chaining: a second, separate LLM call
# the only thing it gets is the booking confirmation from the first call
def draft_invite_message(booking_confirmation: str) -> dict:
    response = client.responses.parse(
        model="gpt-5.2",
        input=[
            {"role": "system", "content": invite_prompt},
            {"role": "user", "content": booking_confirmation},
        ],
        text_format=InviteMessage,
    )
    draft = response.output_parsed
    if draft is None:
        return {"error": "The LLM did not give us a draft back."}

    # model_dump turns the form into a plain dict, so it can go back to the first LLM as JSON
    return draft.model_dump()


# What the LLM sees: a name, a description and the inputs
INVITE_TOOL = {
    "type": "function",
    "name": "draft_invite_message",
    "description": "Write a short invite message for the user's friends about a booking. Only call this once the user has said they want a message drafted.",
    "parameters": {
        "type": "object",
        "properties": {
            "booking_confirmation": {
                "type": "string",
                "description": "The booking confirmation you got from the previous step: the ground, the city, the date, the time slot and the confirmation number",
            },
        },
        "required": ["booking_confirmation"],
    },
}

if __name__ == "__main__":
    print(
        draft_invite_message(
            "slot 10:00-12:00, Hyderabad, 2026-10-31, Rajiv Gandhi International Stadium, booking 123456"
        )
    )
