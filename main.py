from handlers.custom_handlers import history, maximum, minimum, weather
from handlers.default_handlers import echo, help, start
from utils.loader import bot

if __name__ == "__main__":
    bot.infinity_polling()
