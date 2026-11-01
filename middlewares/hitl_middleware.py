from langchain.agents.middleware import HumanInTheLoopMiddleware

ask_before_acting = HumanInTheLoopMiddleware(
    interrupt_on={
        "book_slot": {"allowed_decisions": ["approve", "reject"]},
        "send_email": {"allowed_decisions": ["approve", "reject"]},
    },
    interrupt_mode="per_call",
)
