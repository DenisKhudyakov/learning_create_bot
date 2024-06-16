import logging

from telebot.types import Message

from database.database import get_weather
from utils.loader import bot

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
    weather_data = get_weather(city)
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
        bot.reply_to(message, "Не удалось получить данные о погоде")
