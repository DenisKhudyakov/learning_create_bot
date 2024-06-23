import logging

from telebot.types import Message

from config_data.config import CITIES
from database.database import get_weather_in_bd
from utils.loader import bot
from utils.misc.coordinates import get_coordinates
from utils.weather import get_weather

logging.basicConfig(level=logging.DEBUG)


@bot.message_handler(commands=["weather"])
def bot_weather(message: Message):
    logging.debug(f"Received message: {message.text}")
    args = message.text.split(" ", 1)
    logging.debug(f"Args: {args}")

    if len(args) < 2:
        bot.reply_to(message, "Пожалуйста, введите название города")
        return

    city = args[1].strip()
    logging.debug(f"City: {city}")

    # Замените get_weather на get_weather_from_db
    weather_data = get_weather_in_bd(city)
    logging.debug(f"Weather data: {weather_data}")

    if weather_data:
        bot.reply_to(
            message,
            f"""
Погода в {city}:
Температура: {weather_data['temp']}°C
Давление: {weather_data['pressure']} hPa
Уровень земли: {weather_data['grnd_level']} hPa
            """,
        )
    else:
        CITIES.append(city) # если город не найден в БД, то мы добавим его в в избранное и обращаемся напрямую к API
        lat, lon = get_coordinates(city)
        weather_data = get_weather(lat, lon)
        bot.reply_to(
            message,
            f"""
Погода в {city}:
Температура: {weather_data['temp']}°C
Давление: {weather_data['pressure']} hPa
Уровень земли: {weather_data['grnd_level']} hPa
            """,
        )
