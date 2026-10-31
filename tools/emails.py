from langchain.tools import tool

# our friends' email addresses
EMAIL_ADDRESSES = [
    "ravi@gmail.com",
    "suresh@gmail.com",
    "ramesh@gmail.com",
    "mahesh@gmail.com",
    "ganesh@gmail.com",
    "hitesh@gmail.com",
]


# Send the email: pretend, we only print it (a real app would call an email service here)
@tool(
    name_or_callable="send_email",
    description="Send an email to the user's friends. We already have their email addresses, so never ask the user for them.",
)
def send_email(subject: str, email_body: str) -> dict:
    print(f"Sending email to {EMAIL_ADDRESSES}")
    print(f"Subject: {subject}")
    print(email_body)
    return {"success": True, "email_sent_to": EMAIL_ADDRESSES}
