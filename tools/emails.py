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
def send_email(subject: str, email_body: str) -> dict:
    print(f"Sending email to {EMAIL_ADDRESSES}")
    print(f"Subject: {subject}")
    print(email_body)
    return {"success": True, "email_sent_to": EMAIL_ADDRESSES}


# What the LLM sees: a name, a description and the inputs
EMAIL_TOOL = {
    "type": "function",
    "name": "send_email",
    "description": "Send an email to the user's friends. We already have their email addresses, so never ask the user for them.",
    "parameters": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "The subject of the email to the user's friends",
            },
            "email_body": {
                "type": "string",
                "description": "The body of the email to the user's friends",
            },
        },
        "required": ["subject", "email_body"],
    },
}

if __name__ == "__main__":
    print(send_email("Cricket on Saturday!", "See you at 10."))
