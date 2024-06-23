from telebot.types import Message

from utils.loader import bot


@bot.message_handler(commands=["min"])
def bot_start(message: Message):
    pass