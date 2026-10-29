import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import run_tool, llm_tools

load_dotenv()
client = OpenAI()

# the most rounds we allow for one question, so a confused LLM can't loop forever
MAX_ROUNDS = 20


# we call the LLM, run every tool it asks for, and call it again until it has the answer
def ask_llm_with_tools(messages):
    # clone the messages so we don't change the original list
    llm_messages = messages.copy()
    round_number = 1
    while True:
        print(f"--- round {round_number} ---")

        # we send all the messages so far to the LLM

        ## finally messages contain
        ## system prompt, user question, LLM's tool request, tool's output, LLM's next request, etc.

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=llm_messages,
            tools=llm_tools,  ## this is how we tell the LLM what tools it can use
            parallel_tool_calls=False,  ## this tells LLM to ask for ONE tool at a time so we can run the tool and give the response.
        )

        # we remember if the LLM asked for a tool in this round
        asked_for_tool = False

        # we loop through the LLM's output to see if it asked for a tool
        for item in response.output:
            # type function_call means the LLM is asking for a tool
            if item.type == "function_call":
                asked_for_tool = True

                # we convert the arguments from a string to a dict so we can use them in our code
                tool_name = item.name
                tool_args = json.loads(item.arguments)
                print("LLM asks for a tool:", tool_name, tool_args)

                result = run_tool(tool_name, tool_args)
                print("Our code ran the tool:", result)

                # we add the LLM asking for a tool to the list of messages so the LLM can see it in the next call
                llm_messages.append(item)

                # we add the tool's result to the list of messages so the LLM can see it in the next call
                llm_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(
                            result
                        ),  # we convert the result to a string so the LLM can read it
                    }
                )

        # no tool asked means the LLM has its answer, so we return it
        if not asked_for_tool:
            return response.output_text

        round_number += 1

        # too many rounds means something went wrong, so we stop instead of looping forever
        if round_number > MAX_ROUNDS:
            return f"Sorry, I couldn't finish this in {MAX_ROUNDS} rounds."
