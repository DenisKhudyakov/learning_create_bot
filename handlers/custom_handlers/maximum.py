from telebot.types import Message

from database.database import max_temp
from utils.loader import bot


@bot.message_handler(commands=["max"])
def bot_start(message: Message):
    bot.reply_to(message, f"Абсолютный минимум температуры: {max_temp()}!")

