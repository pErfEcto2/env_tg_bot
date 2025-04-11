import telebot
import lib
import config


bot = telebot.TeleBot(config.API_KEY)

@bot.message_handler(commands=["start"])
def start(message):
    lib.exec_query("create table if not exists users (id int, place varchar(64));")
    
    with open(config.PLACES_FILE_PATH) as f:
        places = map(lambda x: x.strip(), f.readlines())

    ans = "Для начала работы, выбери ближайший к тебе корпус (напиши его номер из списка ниже):\n"
    for i, place in enumerate(places):
        ans += f"{i + 1}) {place}\n"
    bot.send_message(message.chat.id, ans, parse_mode="Markdown")
    bot.register_next_step_handler(message, lib.verify_place_choice, bot)


@bot.message_handler(commands=["help"])
def help(message):
    pass

@bot.message_handler(commands=["donation"])
def donation(message):
    pass

@bot.message_handler(commands=["fact"])
def fact(message):
    pass

@bot.message_handler(content_types=["text"])
def test(message):
    pass


bot.infinity_polling()

