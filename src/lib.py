from os import confstr
import config
import telebot
import sqlite3 


int_in_emojies = {str(i): f"{i}\uFE0F\u20E3 " for i in range(10)}

def exec_query(query: str):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return cur.fetchall()

def verify_place_choice(message, bot: telebot.TeleBot, keyboard_after: telebot.types.ReplyKeyboardMarkup):
    with open(config.PLACES_FILE_PATH) as f:
        places = list(map(lambda x: x.strip(), f.readlines()))
    
    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > len(places):
        bot.send_message(message.chat.id, "Неправильный ввод, попробуй еще раз")
        bot.register_next_step_handler(message, verify_place_choice, bot, keyboard_after)
        return

    exec_query(f"""insert into users values ({message.chat.id}, '{places[int(message.text) - 1]}') on conflict (id) do update set place=excluded.place;""")
    
    bot.send_message(message.chat.id, "Понял, принял, записал)", reply_markup=keyboard_after)

def int_to_emoji(n: int) -> str:
    res = ""

    for el in str(n):
        res += int_in_emojies[el]

    return res

def group(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def add_feedback(message, bot):
    exec_query(f"insert into feedbacks (feedback) values ('{message.text}')")
    bot.send_message(message.chat.id, "Записал")

def show_feedbacks(message, bot):
    if message.text != config.SECRET_PASSWORD:
        bot.send_message(message.chat.id, "Неправильный пароль")
        return
    
    feedbacks = exec_query("select feedback from feedbacks;")
    if not feedbacks:
        bot.send_message(message.chat.id, "Пока нет отзывов")
        return

    ans = "Все отзывы:"
    for el in feedbacks:
        ans += f"\n------\n{el[0]}"

    bot.send_message(message.chat.id, ans)


