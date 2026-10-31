from datetime import datetime

from langchain.tools import tool


# The current date and time (no internet needed)
# return the date in the format "Monday, January 01, 2024, 12:00 PM"
@tool(
    name_or_callable="get_current_datetime",
    description="Get the current date and time.",
)
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y, %I:%M %p")
