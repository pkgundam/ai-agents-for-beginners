# we import Literal so we can limit a field to a few allowed words
from typing import Literal

# we import load_dotenv so we can read our secret keys from the .env file
from dotenv import load_dotenv

# we import OpenAI, the class that lets us talk to the LLM 
from openai import OpenAI

# we import BaseModel, the class we build our form on, pydantic checks the filled form for us
from pydantic import BaseModel

# we load the .env file so the OpenAI key is available to our program
load_dotenv()

# we create the client, this is the object we use to call the LLM
client = OpenAI()

# we define the form the LLM must fill, this is called a schema
class ClinicReply(BaseModel):
    # a short summary of what the patient wants
    summary: str
    # intent can only be one of these three words
    intent: Literal["book_appointment", "ask_hours", "other"]
    # the question our assistant should ask next
    next_question: str


# we store the system prompt in a variable, it tells the LLM how to behave and to fill the form
system_prompt = "You are a friendly front-desk assistant for a clinic. Fill every field in the form."

# we tell the user how to use the chat
print("[LOG] Step 2: chat started, type quit to exit")



# we repeat the chat until the user types quit, a while loop keeps running until we break out of it
while True:
    # we ask the user for their message, input() waits until they type and press enter
    user_prompt = input("You: ")

    # we stop the chat when the user types quit, so the program can end
    if user_prompt == "quit":
        print("[LOG] User typed quit, ending the chat")
        break

    messages_going_to_llm = [
        {
            "role": "system",
            "content": system_prompt,
        },
    ]
        
    # we put the system message and the user message in one list, this is what the LLM reads
    messages_going_to_llm.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    print("[LOG] Calling the LLM with a system prompt and the user's message")

    # we use parse instead of create, text_format=ClinicReply tells the LLM to fill our form
    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=messages_going_to_llm,
        text_format=ClinicReply,
    )

    print("[LOG] Got the answer back from the LLM, it is a filled ClinicReply")

    # we take the filled form out of the response, now it is a ClinicReply object, not plain text
    reply = response.output_parsed

    # we print the intent so we can see what the LLM understood
    print("Intent:", reply.intent)

    # we act on the intent, our code decides what to do, not the LLM
    if reply.intent == "book_appointment":
        print("App: start the booking")
    elif reply.intent == "ask_hours":
        print("App: share the clinic hours")
    else:
        print("App: pass it to the front desk")

    # we print the next question so the chat can continue
    print("Bot:", reply.next_question)
