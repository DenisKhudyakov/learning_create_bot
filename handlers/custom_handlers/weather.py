import logging

from telebot.types import Message

from config_data.config import CITIES
from database.database import add_weather, get_weather_from_db, add_user
from utils.loader import bot
from utils.misc.coordinates import get_coordinates
from utils.weather import get_weather

logging.basicConfig(level=logging.DEBUG)


@bot.message_handler(commands=["weather"])
def bot_weather(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.debug(f"Received message: {message.text}")
    args = message.text.split(" ", 1)
    logging.debug(f"Args: {args}")

    if len(args) < 2:
        bot.reply_to(message, "Пожалуйста, введите название города")
        return

    city = args[1].strip()
    logging.debug(f"City: {city}")

    weather_data = get_weather_from_db(city)
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
        CITIES.append(
            city
        )  # если город не найден в БД, то мы добавим его в избранное и обращаемся напрямую к API
        lat, lon = get_coordinates(city)
        weather_data = get_weather(lat, lon)
        temp = weather_data['temp']
        pressure = weather_data['pressure']
        grnd_level = weather_data['grnd_level']
        logging.debug(f"Айди пользователя: {user_id}")
        add_user(user_id=user_id, full_name=user_name)
        add_weather(
            city=city,
            temp=temp,
            pressure=pressure,
            grnd_level=grnd_level,
            user_id=user_id,
        ) # добавляем в БД запрос
        bot.reply_to(
            message,
            f"""
Погода в {city}:
Температура: {temp}°C
Давление: {pressure} hPa
Уровень земли: {grnd_level} hPa
            """,
        )
