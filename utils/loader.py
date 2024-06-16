from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.config.tg_bot.token, state_storage=storage)
