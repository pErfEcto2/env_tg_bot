import telebot
import lib
import config


bot = telebot.TeleBot(config.API_KEY)

commands = [
    "start",
    "help", 
    "feedback", 
    "fact"
]

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Начало работы"), 
    telebot.types.BotCommand("/help", "Помощь"), 
    telebot.types.BotCommand("/feedback", "Оставить отзыв"), 
    telebot.types.BotCommand("/fact", "Показать факт")
])

@bot.message_handler(commands=["start"])
def start(message):
    with open(config.PLACES_FILE_PATH) as f:
        places = map(lambda x: x.strip(), f.readlines())

    ans = "Для начала работы, выбери ближайший к тебе корпус *(напиши его номер из списка ниже)*:\n\n"
    for i, place in enumerate(places):
        ans += f"{lib.int_to_emoji(i + 1)} - {place}\n"
    bot.send_message(message.chat.id, ans, parse_mode="Markdown")
    bot.register_next_step_handler(message, lib.verify_place_choice, bot)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "заглушка для help")


@bot.message_handler(commands=["feedback"])
def feedback(message):
    bot.send_message(message.chat.id, "заглушка для feedback")


@bot.message_handler(commands=["fact"])
def fact(message):
    bot.send_message(message.chat.id, "заглушка для fact")


@bot.message_handler(content_types=["text"])
def test(message):
    bot.send_message(message.chat.id, "заглушка для сообщений")


bot.infinity_polling()

