from telebot.types import Message

from utils.loader import bot


@bot.message_handler(func=lambda message: True, state=None)
def bot_echo(message: Message):
    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
