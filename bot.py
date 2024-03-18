import os
from dotenv import load_dotenv
from telebot import TeleBot

from info import (
    character_mapping,
    start_massage,
    images_info,
    info_message1,
    info_message2,
    questions,
    warning_message
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, start_massage)


@bot.message_handler(commands=['quiz'])
def quiz_bot(message):
    chat_id = message.chat.id
    current_questions = questions.copy()
    points = 0
    ask_question(chat_id, message, current_questions, points)


def ask_question(chat_id, message, remaining_question, points):
    if len(remaining_question) > 0:
        question = remaining_question[0]
        bot.send_message(message.chat.id, question["question"])
        options = question["options"]
        for option_number, option in options.items():
            bot.send_message(chat_id, f"{option_number}. {option['text']}")

        bot.register_next_step_handler(message, process_answer, remaining_question, points)
    else:
        character = ""
        for own_points, char in character_mapping.items():
            if own_points[0] <= points <= own_points[1]:
                character = char
                break

        result = {
            "points": points,
            "character": character
        }

        if result["character"] in images_info:
            images_path = images_info[result["character"]]
            bot.send_photo(
                message.chat.id,
                open(images_path, 'rb'),
                caption=f"Вы набрали {result['points']} очков. Вам подходит: {result['character']}")


def process_answer(message, remaining_questions, current_points):
    chat_id = message.chat.id
    answer = message.text
    if answer.isdigit() and int(answer) in remaining_questions[0]["options"]:
        current_points += remaining_questions[0]["options"][int(answer)]["points"]
        remaining_questions.pop(0)
        ask_question(chat_id, message, remaining_questions, current_points)
    elif answer == '/start':
        bot.send_message(message.chat.id, info_message1)
        return
    else:
        bot.send_message(message.chat.id, info_message2)
        ask_question(chat_id, message, remaining_questions, current_points)


@bot.message_handler(content_types=['text'])
def text_message(message):
    bot.send_message(message.chat.id, warning_message)


bot.polling()
