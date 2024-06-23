from handlers.custom_handlers import weather, maximum, minimum, history
from handlers.default_handlers import help, start, echo
from utils.loader import bot

if __name__ == "__main__":
    bot.infinity_polling()
