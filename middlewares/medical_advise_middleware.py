from langchain.agents import create_agent
from langchain.agents.middleware import after_model
from langchain.messages import AIMessage, HumanMessage
from pydantic import BaseModel

SAFE_REPLY = (
    "I can't give medical advice. Please call your doctor or pharmacist, "
    "or go to urgent care if it's serious. I can help you book an appointment."
)


## structured output class which is a pydantic model.
class AdviceCheck(BaseModel):
    gives_medical_advice: bool


## medical advise LLM call prompt
CHECK_PROMPT = (
    "You check replies from a clinic front-desk assistant. "
    "gives_medical_advice is true only if the reply tells the patient to use a specific medicine, "
    "a dose, or a treatment or anything that looks like asking the patient or encouraging the patient to take any medicine "
    "Telling them to contact a doctor, a pharmacist or urgent care is not medical advice."
)

checker = create_agent(
    model="openai:gpt-5.4-mini",
    system_prompt=CHECK_PROMPT,
    response_format=AdviceCheck,
)


def gives_medical_advice(reply: str) -> bool:
    result = checker.invoke({"messages": [HumanMessage(reply)]})
    check: AdviceCheck = result["structured_response"]
    return check.gives_medical_advice


@after_model
def block_medical_advice(state, runtime):
    print("[AFTER MODEL] block_medical_advice checks the reply")
    last = state["messages"][-1]  ## get the most recent message
    ## this has to be an AI message and it should not be a tool call request
    if last.type != "ai" or last.tool_calls:
        return None

    ## else, this is an AI message

    llm_response = last.content
    ## we need to check if there is a medical advise in llm_response
    ## we do it using another LLM call just to verify if this text contains a medical advise
    ## we want it to respond with a true or false
    ## if true, we want to replace llm_response with a safer message which is not a medical advise.
    print(" ======= ORIGINAL LLM response")
    print(llm_response)
    print(" ======= ORIGINAL LLM response")
    print()
    print()
    print()

    contains_medical_advise = gives_medical_advice(llm_response)
    print("========== contains_medical_advise ===========")
    print(f"contains_medical_advise: {contains_medical_advise}")
    print("========== contains_medical_advise ===========")
    if not contains_medical_advise:
        return None

    print(f"[MIDDLEWARE] block_medical_advice replaced: {last.content}")
    return {
        "messages": [AIMessage("owr own response to replace llm_message", id=last.id)]
    }
