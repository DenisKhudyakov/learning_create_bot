<<<<<<< HEAD
import telebot
import config
bot = telebot.TeleBot(config.BOT_TOKEN)
@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.reply_to(message, "Добрый день ,Я бот помощник. Что желаете?")
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.reply_to(message, "Привет")
    elif message.text == "/help":
        bot.reply_to(message, "Чем Я могу помочь?")
    else:
        bot.reply_to(message, "Я тебя не понимаю. Напиши /help.")

bot.infinity_polling()
=======
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)

>>>>>>> 8ab09d1 (init template)
