from .cities import CITIES_TOOL, get_available_cities
from .date_time import DATE_TIME_TOOL, get_current_datetime
from .emails import EMAIL_TOOL, send_email
from .forecast import FORECAST_TOOL, get_weather_for_city_and_date
from .invite import INVITE_TOOL, draft_invite_message
from .news import NEWS_TOOL, get_top_news
from .remember import REMEMBER_TOOL, remember
from .slots import (
    BOOK_SLOT_TOOL,
    SLOT_AVAILABLE_TOOL,
    SLOTS_TOOL,
    book_slot,
    get_all_slots,
    is_slot_available,
)
from .stocks import STOCK_TOOL, get_stock_price
from .weather import WEATHER_TOOL, get_weather

## schemas of all the tools we have, so these get registered with the LLM
# and it knows what they do and how to call them
llm_tools = [
    DATE_TIME_TOOL,
    WEATHER_TOOL,
    STOCK_TOOL,
    NEWS_TOOL,
    REMEMBER_TOOL,
    ## cricket booking tools
    CITIES_TOOL,
    FORECAST_TOOL,
    SLOTS_TOOL,
    SLOT_AVAILABLE_TOOL,
    BOOK_SLOT_TOOL,
    INVITE_TOOL,
    EMAIL_TOOL,
]


# Our code runs the tool the LLM asked for
def run_tool(name, args):
    if name == "get_current_datetime":
        print("[TOOL] get_current_datetime()")
        return get_current_datetime()
    if name == "get_weather":
        print("[TOOL] get_weather()")
        return get_weather(args["city"])
    if name == "get_stock_price":
        print("[TOOL] get_stock_price()")
        return get_stock_price(args["symbol"])
    if name == "get_top_news":
        print("[TOOL] get_top_news()")
        return get_top_news()
    if name == "remember":
        print("[TOOL] remember()")
        return remember(args["type"], args["key"], args["value"])
    ## cricket booking tools
    if name == "get_available_cities":
        print("[TOOL] get_available_cities()")
        return get_available_cities()
    if name == "get_weather_for_city_and_date":
        print("[TOOL] get_weather_for_city_and_date()")
        return get_weather_for_city_and_date(args["city"], args["date"])
    if name == "get_all_slots":
        print("[TOOL] get_all_slots()")
        return get_all_slots(args["city"], args["date"])
    if name == "is_slot_available":
        print("[TOOL] is_slot_available()")
        return is_slot_available(args["time_window"])
    if name == "book_slot":
        print("[TOOL] book_slot()")
        return book_slot(
            args["time_window"], args["city"], args["date"], args["ground"]
        )
    if name == "draft_invite_message":
        print("[TOOL] draft_invite_message()")
        return draft_invite_message(args["booking_confirmation"])
    if name == "send_email":
        print("[TOOL] send_email()")
        return send_email(args["subject"], args["email_body"])
