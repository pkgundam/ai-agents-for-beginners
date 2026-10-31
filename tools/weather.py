import requests
from langchain.tools import tool


# The weather in a city
@tool(name_or_callable="get_weather", description="Get the current weather in a city.")
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
