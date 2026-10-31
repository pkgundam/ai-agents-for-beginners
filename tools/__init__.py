from .cities import get_available_cities
from .date_time import get_current_datetime
from .emails import send_email
from .forecast import get_weather_for_city_and_date
from .invite import draft_invite_message
from .news import get_top_news
from .remember import remember
from .slots import (
    book_slot,
    get_all_slots,
    is_slot_available,
)
from .stocks import get_stock_price
from .weather import get_weather

lc_tools = [
    get_weather,
    get_stock_price,
    get_top_news,
    book_slot,
    get_all_slots,
    is_slot_available,
    remember,
    draft_invite_message,
    get_weather_for_city_and_date,
    send_email,
    get_current_datetime,
    get_available_cities,
]
