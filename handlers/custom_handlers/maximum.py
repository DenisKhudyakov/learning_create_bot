from telebot.types import Message

from utils.loader import bot


@bot.message_handler(commands=["max"])
def bot_start(message: Message):
    pass