from utils.loader import bot
from handlers.custom_handlers import weather
from handlers.default_handlers import help, start, echo


if __name__ == "__main__":
    bot.infinity_polling()
