from langchain.tools import tool

# The cities we have cricket grounds in
CITIES = ["Mumbai", "Chennai", "Hyderabad", "Jaipur", "Bengaluru"]


@tool(
    name_or_callable="get_available_cities",
    description="Get the cities we have cricket grounds in. Call this before asking the user which city they want.",
)
def get_available_cities() -> dict:
    return {"cities": CITIES}
