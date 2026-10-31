import random

from langchain.tools import tool

# one ground per city
GROUNDS = {
    "mumbai": "Wankhede Stadium",
    "chennai": "M. A. Chidambaram Stadium",
    "hyderabad": "Rajiv Gandhi International Stadium",
    "jaipur": "Sawai Mansingh Stadium",
    "bengaluru": "M. Chinnaswamy Stadium",
}

# all the slots, including the ones already taken (on purpose, so we can see the availability check)
SLOTS = [
    {"time_window": "06:00-08:00"},
    {"time_window": "08:00-10:00"},
    {"time_window": "10:00-12:00"},
    {"time_window": "14:00-16:00"},
    {"time_window": "16:00-18:00"},
    {"time_window": "18:00-20:00"},
]

# only the slots that are still free
AVAILABLE_SLOTS = ["10:00-12:00", "16:00-18:00", "18:00-20:00"]


# The ground for a city, and all its slots on a date
@tool(
    name_or_callable="get_all_slots",
    description="Get the ground for a city and all its time slots on a date.",
)
def get_all_slots(city: str, date: str) -> dict:
    ground = GROUNDS.get(city.strip().lower())
    if ground is None:
        return {"error": f"We do not have a ground in {city}."}
    return {"city": city.title(), "date": date, "ground": ground, "slots": SLOTS}


# Is this slot still free?
@tool(
    name_or_callable="is_slot_available",
    description="Check if a slot is available for the given time window.",
)
def is_slot_available(time_window: str) -> dict:
    return {"is_available": time_window in AVAILABLE_SLOTS}


# Book a slot: this tool changes something, so it only succeeds if the slot is really free
@tool(
    name_or_callable="book_slot",
    description="Book a slot for a given time window, city, date and ground.",
)
def book_slot(time_window: str, city: str, date: str, ground: str) -> dict:
    if time_window not in AVAILABLE_SLOTS:
        return {
            "success": False,
            "slot": time_window,
            "reason": "This slot is already taken.",
        }

    # the slot is ours now, so nobody else can book it
    AVAILABLE_SLOTS.remove(time_window)
    return {
        "success": True,
        "slot": time_window,
        "city": city.title(),
        "date": date,
        "ground": ground,
        "booking_conf_number": random.randint(100000, 999999),
    }
