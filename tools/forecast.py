import random

# pretend forecasts: we pick one at random
# (a real weather API would use the city and the date, but the workflow is what we are here to learn)
FORECASTS = [
    {"description": "clear sky", "max_temp_c": 31, "chance_of_rain_percent": 0},
    {"description": "partly cloudy", "max_temp_c": 29, "chance_of_rain_percent": 10},
    {"description": "partly cloudy", "max_temp_c": 30, "chance_of_rain_percent": 15},
    {"description": "overcast", "max_temp_c": 32, "chance_of_rain_percent": 20},
    # uncomment these to see the workflow stop at step 3 because of bad weather
    # {"description": "heavy rain", "max_temp_c": 28, "chance_of_rain_percent": 95},
    # {"description": "heavy rain", "max_temp_c": 28, "chance_of_rain_percent": 90},
]


# The weather in one of our cities on a date
def get_weather_for_city_and_date(city: str, date: str) -> dict:
    weather = random.choice(FORECASTS)
    return {
        "city": city.title(),
        "date": date,
        "description": weather["description"],
        "max_temp_c": weather["max_temp_c"],
        "chance_of_rain_percent": weather["chance_of_rain_percent"],
    }


# What the LLM sees: a name, a description and the inputs
FORECAST_TOOL = {
    "type": "function",
    "name": "get_weather_for_city_and_date",
    "description": "Get the weather for one of our cities on a date. Call this before deciding whether cricket can be played.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "A city from get_available_cities",
            },
            "date": {
                "type": "string",
                "description": "The date you want, as YYYY-MM-DD",
            },
        },
        "required": ["city", "date"],
    },
}

if __name__ == "__main__":
    print(get_weather_for_city_and_date("Hyderabad", "2026-10-31"))
