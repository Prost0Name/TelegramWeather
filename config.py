import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

if not BOT_TOKEN:
    raise ValueError("Не задана переменная окружения BOT_TOKEN")
    
if not OPENWEATHER_API_KEY:
    raise ValueError("Не задана переменная окружения OPENWEATHER_API_KEY") 