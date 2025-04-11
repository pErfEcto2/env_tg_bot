import config
import telebot
import sqlite3 


def exec_query(query: str):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return cur.fetchall()


def verify_place_choice(message, bot: telebot.TeleBot):
    with open(config.PLACES_FILE_PATH) as f:
        places = list(map(lambda x: x.strip(), f.readlines()))
    
    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > len(places):
        bot.send_message(message.chat.id, "Неправильный ввод, попробуй еще раз")
        bot.register_next_step_handler(message, verify_place_choice, bot)
        return

    exec_query(f"""insert or replace into users (id, place) values ({message.chat.id}, '{int(message.text) - 1}')""")
    bot.send_message(message.chat.id, "Понял, принял, запомнил)")

def int_to_emoji(n: int) -> str:
    res = ""

    for el in str(n):
        res += f"{el}\uFE0F\u20E3 "

    return res


