from .date_time import DATE_TIME_TOOL, get_current_datetime
from .news import NEWS_TOOL, get_top_news
from .remember import REMEMBER_TOOL, remember
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
]


# Our code runs the tool the LLM asked for
def run_tool(name, args):
    if name == "get_current_datetime":
        return get_current_datetime()
    if name == "get_weather":
        return get_weather(args["city"])
    if name == "get_stock_price":
        return get_stock_price(args["symbol"])
    if name == "get_top_news":
        return get_top_news()
    if name == "remember":
        return remember(args["type"], args["key"], args["value"])
