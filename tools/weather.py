import requests


# The weather in a city
def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"
    data = requests.get(url, timeout=10).json()
    current = data["current_condition"][0]
    return {
        "city": city,
        "temperature_f": current["temp_F"],
        "feels_like_f": current["FeelsLikeF"],
        "description": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
    }


# What the LLM sees: a name, a description and the inputs
# this is called a schema, and it is how the LLM knows what the tool does and how to call it
WEATHER_TOOL = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather in a city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string", 
                "description": "The name of the city, for example Atlanta"
            },
        },
        "required": ["city"],
    },
}

if __name__ == "__main__":
    city = "Mumbai"
    print(f"Getting the weather in {city}...")
    weather = get_weather(city)
    print(weather)