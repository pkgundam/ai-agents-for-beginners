from datetime import datetime


# The current date and time (no internet needed)
# return the date in the format "Monday, January 01, 2024, 12:00 PM"
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y, %I:%M %p")

# What the LLM sees: a name, a description and the inputs
## this is called a schema,
# this is what gets registered with the LLM 
# and it is how the LLM knows what the tool does and how to call it
# by the name, description, and parameters
DATE_TIME_TOOL = {
    "type": "function",
    "name": "get_current_datetime",
    "description": "Get the current date and time.",
    "parameters": {
        "type": "object", 
        "properties": {}, 
        "required": []
    },
}

if __name__ == "__main__":
    print(get_current_datetime())
