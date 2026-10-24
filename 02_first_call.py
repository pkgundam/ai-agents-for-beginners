# we import load_dotenv so we can read our secret keys from the .env file
from dotenv import load_dotenv

# we import OpenAI, the class that lets us talk to the LLM
from openai import OpenAI

# we load the .env file so the OpenAI key is available to our program
load_dotenv()

# we create the client, this is the object we use to call the LLM
client = OpenAI()

# Method 1 is commented out, we now use Method 2 as a chatbot
# # we store our question in a variable so it is easy to read and change later
# user_prompt = "In one sentence, what is a large language model?"
#
# # Method 1: only a user prompt, no system prompt
# print("[LOG] Method 1: calling the LLM with only a user prompt")
#
# # we call the LLM and keep its reply in response, this call is the heart of the program
# response = client.responses.create(
#     model="gpt-4.1-mini",
#     input=user_prompt,
# )
#
# print("[LOG] Got the answer back from the LLM")
#
# # we print the label and then the text of the answer so we can see what the LLM said
# print("Method 1:")
# print(response.output_text)

# we store the system prompt in a variable, it tells the LLM how to behave
system_prompt = "You are a friendly teacher. Explain things so a 10-year-old can understand, in one short sentence."

# Method 2: a chatbot with a system prompt, the user types the questions
print("[LOG] Method 2: chat started, type quit to exit")

# we repeat the chat until the user types quit, a while loop keeps running until we break out of it
while True:
    # we ask the user for their question, input() waits until they type and press enter
    user_prompt = input("You: ")

    # we stop the chat when the user types quit, so the program can end
    if user_prompt == "quit":
        print("[LOG] User typed quit, ending the chat")
        break

    print("[LOG] Calling the LLM with a system prompt and the user's question")

    # we send a list of messages, each message has a role, this is how the LLM knows who said what
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    print("[LOG] Got the answer back from the LLM")

    # we print the answer so it looks like a reply in a chat
    print("Bot:", response.output_text)
