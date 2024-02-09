from telebot import TeleBot

bot = TeleBot('6556877111:AAGpsvvulvRTTMrWpoVapTMelSzEhyxBPH4')

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, 'Привет, добро пожаловать в бот анкету!')
