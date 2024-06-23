from telebot.types import Message

from database.database import min_temp
from utils.loader import bot


@bot.message_handler(commands=["min"])
def bot_start(message: Message):
    bot.reply_to(message, f"Абсолютный минимум температуры: {min_temp()}!")

