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
    "Пластмассовые бутылки 🫙",
    "Алюминиевые банки 🥫", 
    "Крышки от бутылок 🔴",
    "Аккумуляторы/ашки 🔋",
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

    buildings = list(map(lambda x: x[0], lib.exec_query("select address from buildings")))

    ans = "Выбери ближайший к тебе корпус *(напиши его номер из списка ниже)*:\n\n"
    for i, building in enumerate(buildings):
        ans += f"{lib.int_to_emoji(i + 1)} - {building}\n"
    
    nums_keyboard = telebot.types.ReplyKeyboardMarkup()
    for row in lib.group(range(1, len(buildings) + 1), 4):
        nums_keyboard.add(*list(map(lambda x: str(x), row)), row_width=4)
    nums_keyboard.add("Отмена")
    
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
    
    bot.send_message(message.chat.id, "Сейчас можешь написать свои впечатления от бота или какие-нибудь пожелания")
    bot.register_next_step_handler(message, lib.add_feedback, bot)


@bot.message_handler(commands=["fact"])
def fact(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return
    
    bot.send_message(message.chat.id, "Интересный факт ♻️\n\n" + random.choice(facts), reply_markup=main_keyboard)


@bot.message_handler(commands=["show_feedbacks"])
def show_feedbacks(message):
    bot.send_message(message.chat.id, "Введи супер-секретный пароль")
    bot.register_next_step_handler(message, lib.show_feedbacks, bot)


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.chat.id == config.MONITOR_CHAT_ID:
        return

    if not lib.exec_query(f"select * from users where id = {message.chat.id};"):
        start(message)
        return
    
    table = ""
    
    match message.text:
        case "Пластмассовые бутылки 🫙":
            table = "plastic"

        case "Алюминиевые банки 🥫":
            table = "metall"
            
        case "Крышки от бутылок 🔴":
            table = "caps"
        
        case "Аккумуляторы/ашки 🔋":
            table = "battaries"

        case "Где я?":
            building = lib.exec_query(f"select address from users u join buildings b on u.building_id = b.id where u.id = {message.chat.id}")[0][0]
            bot.send_message(message.chat.id, f"У тебя выбран адрес:\n{building}", reply_markup=main_keyboard)

        case "Поменять корпус":
            start(message)
        
    if message.text in main_keyboard_buttons[:4]:
        data = lib.exec_query(f"select description, address from {table} p join users u using (building_id) where u.id = {message.chat.id}")
        lib.send_addresses(message.chat.id, bot, data)

bot.infinity_polling()

