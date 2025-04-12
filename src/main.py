import telebot
import lib
import config
import random


bot = telebot.TeleBot(config.API_KEY)

commands = [
    "start",
    "help", 
    "feedback", 
    "fact"
]

main_keyboard_rows = [
    "Сдать пластмассовые бутылки",
    "Сдать алюминиевые банки", 
    "Сдать крышки от бутылок"
]

help_text = """Привет!
Я – чат-бот, который поможет тебе найти ближайшие пункты приема пластмассовых бутылок, алюминиевых банок и крышек рядом с твоим корпусом.

У меня всего 4 команды:
1) /start - для начала работы и выбора корпуса
2) /help - выводит это сообщение
3) /feedback - можешь оставить свой фидбек
4) /fact - показать интересный факт
"""

with open(config.FACTS_FILE_PATH, "r") as f:
    facts = list(map(lambda x: x.strip(), f.readlines()))

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начало работы"), 
    telebot.types.BotCommand("/help", "Помощь"), 
    telebot.types.BotCommand("/feedback", "Оставить отзыв"), 
    telebot.types.BotCommand("/fact", "Прикольный факт")
])

main_keyboard = telebot.types.ReplyKeyboardMarkup()
main_keyboard.add(*main_keyboard_rows, row_width=1)


@bot.message_handler(commands=["start"])
def start(message):
    with open(config.PLACES_FILE_PATH, "r") as f:
        places = list(map(lambda x: x.strip(), f.readlines()))

    ans = "Для начала работы, выбери ближайший к тебе корпус *(напиши его номер из списка ниже)*:\n\n"
    for i, place in enumerate(places):
        ans += f"{lib.int_to_emoji(i + 1)} - {place}\n"
    
    nums_keyboard = telebot.types.ReplyKeyboardMarkup()
    for row in lib.group(range(1, len(places) + 1), 4):
        nums_keyboard.add(*list(map(lambda x: str(x), row)), row_width=4)
    
    bot.send_message(message.chat.id, ans, parse_mode="Markdown", reply_markup=nums_keyboard)
    bot.register_next_step_handler(message, lib.verify_place_choice, bot, main_keyboard)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, help_text, reply_markup=main_keyboard, parse_mode="Markdown")


@bot.message_handler(commands=["feedback"])
def feedback(message):
    bot.send_message(message.chat.id, "Сейчас можешь написать свои впечатления от бота или какие-нибудь пожелания")
    bot.register_next_step_handler(message, lib.add_feedback, bot)


@bot.message_handler(commands=["fact"])
def fact(message):
    bot.send_message(message.chat.id, random.choice(facts))


@bot.message_handler(commands=["show_feedbacks"])
def show_feedback(message):
    bot.send_message(message.chat.id, "Введи супер-секретный пароль")
    bot.register_next_step_handler(message, lib.show_feedbacks, bot)


@bot.message_handler(content_types=["text"])
def test(message):
    bot.send_message(message.chat.id, "заглушка для сообщений")


bot.infinity_polling()

