# The cities we have cricket grounds in
CITIES = ["Mumbai", "Chennai", "Hyderabad", "Jaipur", "Bengaluru"]


def get_available_cities() -> dict:
    return {"cities": CITIES}


# Schema of the tool we have, so this gets registered with the LLM
CITIES_TOOL = {
    "type": "function",
    "name": "get_available_cities",
    "description": "Get the cities we have cricket grounds in. Call this before asking the user which city they want.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

if __name__ == "__main__":
    print(get_available_cities())
