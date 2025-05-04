import aiohttp
from config import OPENWEATHER_API_KEY, OPENWEATHER_API_URL

async def get_weather(city: str) -> str:
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',  
        'lang': 'ru'  
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(OPENWEATHER_API_URL, params=params) as response:
            if response.status != 200:
                raise Exception(f"Не удалось получить данные о погоде. Код ошибки: {response.status}")
            
            data = await response.json()
            
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind_speed = data['wind']['speed']
            
            weather_info = (
                f"🏙 Погода в городе {city}:\n\n"
                f"🌡 Температура: {temperature}°C\n"
                f"🌡 Ощущается как: {feels_like}°C\n"
                f"☁️ Описание: {weather_description}\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌪 Скорость ветра: {wind_speed} м/с\n"
                f"🔵 Давление: {pressure} гПа"
            )
            
            return weather_info 

async def get_weather_by_coords(lat: float, lon: float) -> str:
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(OPENWEATHER_API_URL, params=params) as response:
            if response.status != 200:
                raise Exception(f"Не удалось получить данные о погоде. Код ошибки: {response.status}")
            data = await response.json()
            city = data.get('name', 'вашем регионе')
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind_speed = data['wind']['speed']
            weather_info = (
                f"🏙 Погода в {city} (по координатам):\n\n"
                f"🌡 Температура: {temperature}°C\n"
                f"🌡 Ощущается как: {feels_like}°C\n"
                f"☁️ Описание: {weather_description}\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌪 Скорость ветра: {wind_speed} м/с\n"
                f"🔵 Давление: {pressure} гПа"
            )
            return weather_info 