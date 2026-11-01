# from .medical_advise_middleware import block_medical_advice
from .hitl_middleware import ask_before_acting
from .middleware import (
    log_after_agent,
    # log_after_model,
    log_before_agent,
    # log_before_model,
    log_wrap_model_call,
    log_wrap_tool_call,
)
from .rolling_summary_middleware import summarize_old_messages
from .ssn_middleware import redact_ssn

middleware_methods = [
    log_after_agent,
    # log_after_model,
    log_before_agent,
    # log_before_model,
    log_wrap_model_call,
    log_wrap_tool_call,
    redact_ssn,
    # block_medical_advice,
    summarize_old_messages,
    ask_before_acting,
]
