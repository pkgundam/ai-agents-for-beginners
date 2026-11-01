from langchain.agents.middleware import (
    after_agent,
    # after_model,
    before_agent,
    before_model,
    wrap_model_call,
    wrap_tool_call,
)


@before_agent
def log_before_agent(state, runtime):
    print("[BEFORE AGENT] the agent is starting")


# @before_model
# def log_before_model(state, runtime):
# message = state["messages"][-1]
# print(f"[BEFORE MODEL] message going to llm: {message.type}, {message.content}")


@wrap_model_call
def log_wrap_model_call(request, handler):
    print("[WRAP MODEL CALL] calling the model")
    response = handler(request)
    print("[WRAP MODEL CALL] the model answered")
    return response


# @after_model
# def log_after_model(state, runtime):
#     message = state["messages"][-1]
#     print(f"[AFTER MODEL] message from the llm: {message.type}, {message.content}")


@wrap_tool_call
def log_wrap_tool_call(request, handler):
    print(f"[WRAP TOOL CALL] running {request.tool_call['name']}")
    result = handler(request)
    print(f"[WRAP TOOL CALL] {request.tool_call['name']} is done")
    return result


@after_agent
def log_after_agent(state, runtime):
    print("[AFTER AGENT] the agent is done")
