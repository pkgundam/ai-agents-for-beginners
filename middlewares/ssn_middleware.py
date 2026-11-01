import re

from langchain.agents.middleware import before_model
from langchain.messages import HumanMessage

SSN_PATTERN = re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b")


@before_model
def redact_ssn(state, runtime):
    print("[BEFORE MODEL] redact_ssn checks the message")
    last = state["messages"][
        -1
    ]  ## here is the most recent message from the list of messages.
    if last.type != "human":
        return None

    redacted = SSN_PATTERN.sub("[REDACTED SSN]", last.content)
    if redacted == last.content:
        return None

    print(f"[MIDDLEWARE] redact_ssn: {redacted}")
    return {"messages": [HumanMessage(redacted, id=last.id)]}
