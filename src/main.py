from os import stat
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

main_keyboard_buttons = [
    "Сдать пластмассовые бутылки 🫙",
    "Сдать алюминиевые банки 🥫", 
    "Сдать крышки от бутылок 🔴",
    "Сдать аккумуляторы/ашки 🔋",
    "Где я?",
    "Поменять корпус"
]

help_text = """Привет!
Я – чат-бот, который поможет тебе найти ближайшие пункты приема пластмассовых бутылок, алюминиевых банок и крышек рядом с твоим корпусом.

У меня есть 4 команды:
1) /start - для выбора корпуса
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
    telebot.types.BotCommand("/fact", "Факт")
])

main_keyboard = telebot.types.ReplyKeyboardMarkup()
main_keyboard.add(*main_keyboard_buttons[:4], row_width=2)
main_keyboard.add(main_keyboard_buttons[4])
main_keyboard.add(main_keyboard_buttons[5])


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return

    with open(config.PLACES_FILE_PATH, "r") as f:
        buildings = list(map(lambda x: x.strip(), f.readlines()))

    ans = "Выбери ближайший к тебе корпус *(напиши его номер из списка ниже)*:\n\n"
    for i, building in enumerate(buildings):
        ans += f"{lib.int_to_emoji(i + 1)} - {building}\n"
    
    nums_keyboard = telebot.types.ReplyKeyboardMarkup()
    for row in lib.group(range(1, len(buildings) + 1), 4):
        nums_keyboard.add(*list(map(lambda x: str(x), row)), row_width=4)
    
    bot.send_message(message.chat.id, ans, parse_mode="Markdown", reply_markup=nums_keyboard)
    bot.register_next_step_handler(message, lib.verify_building_choice, bot, main_keyboard)


@bot.message_handler(commands=["help"])
def help(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return
    
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


@bot.message_handler(commands=["feedback"])
def feedback(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return
    
    bot.send_message(message.chat.id, "Сейчас можешь написать свои впечатления от бота или какие-нибудь пожелани")
    bot.register_next_step_handler(message, lib.add_feedback, bot)


@bot.message_handler(commands=["fact"])
def fact(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return
    
    bot.send_message(message.chat.id, "Интересный факт ♻️\n\n" + random.choice(facts), reply_markup=main_keyboard)


@bot.message_handler(commands=["show_feedbacks"])
def show_feedbacks(message):
    bot.send_message(message.chat.id, "Введи супер-секретный пароль", reply_markup=main_keyboard)
    bot.register_next_step_handler(message, lib.show_feedbacks, bot)


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return

    if not lib.exec_query(f"select * from users where id = {message.chat.id};"):
        start(message)
        return
    
    match message.text:
        case "Сдать пластмассовые бутылки 🫙":
            bot.send_message(message.chat.id, "сдаем пластмассовые бутылки 🫙")
            
        case "Сдать алюминиевые банки 🥫":
            bot.send_message(message.chat.id, "сдаем алюминиевые банки 🥫")
            
        case "Сдать крышки от бутылок 🔴":
            bot.send_message(message.chat.id, "сдаем крышки от бутылок 🔴")
        
        case "Сдать аккумуляторы/ашки 🔋":
            bot.send_message(message.chat.id, "сдаем аккумуляторы 🔋")

        case "Где я?":
            building = lib.exec_query(f"select building from users where id = {message.chat.id}")[0][0]
            bot.send_message(message.chat.id, f"У тебя выбран адрес:\n{building}", reply_markup=main_keyboard)

        case "Поменять корпус":
            start(message)
        

bot.infinity_polling()

