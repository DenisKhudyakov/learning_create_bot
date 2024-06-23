from telebot.types import Message

from database.database import get_weather_history
from utils.loader import bot


@bot.message_handler(commands=["history"])
def bot_start(message: Message) -> None:
    user_id = message.from_user.id
    history = get_weather_history(user_id=user_id)
    if history:
        for record in history:
            bot.reply_to(message,
                         f"Погода в {record.city}: {record.temp}°C, Pressure: {record.pressure}, Ground Level: {record.grnd_level}")
    else:
        bot.reply_to(message, "История погоды не найдена.")
