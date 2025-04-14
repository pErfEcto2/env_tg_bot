import config
import telebot
import sqlite3 


int_in_emojies = {str(i): f"{i}\uFE0F\u20E3 " for i in range(10)}

def exec_query(query: str):
    if query is None:
        return

    with sqlite3.connect(config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        res = cur.fetchall()

    return res

def verify_building_choice(message, bot: telebot.TeleBot, keyboard_after: telebot.types.ReplyKeyboardMarkup):
    if message.text is None:
        bot.send_message(message.chat.id, "Отправь, пожалуйста, сообщение текстом:")
        bot.register_next_step_handler(message, verify_building_choice, bot, keyboard_after)
        return

    with open(config.PLACES_FILE_PATH) as f:
        buildings = list(map(lambda x: x.strip(), f.readlines()))
    
    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > len(buildings):
        bot.send_message(message.chat.id, "Неправильный ввод, попробуй еще раз")
        bot.register_next_step_handler(message, verify_building_choice, bot, keyboard_after)
        return

    is_old_user = bool(exec_query(f"select 1 from users where id = {message.chat.id};"))
    if not is_old_user:
        n = exec_query("select count(*) from users;")[0][0]
        bot.send_message(config.MONITOR_CHAT_ID, f"Новый пользователь добавлен\nТеперь их {n + 1}")

    exec_query(f"""insert into users values ({message.chat.id}, '{int(message.text)}') on conflict (id) do update set building_id = excluded.building_id;""")
    
    bot.send_message(message.chat.id, "Выбери тип отходов:", reply_markup=keyboard_after)

def int_to_emoji(n: int) -> str:
    res = ""

    for el in str(n):
        res += int_in_emojies[el]

    return res

def group(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def add_feedback(message, bot):
    if message.text is None:
        bot.send_message(message.chat.id, "Отправь, пожалуйста, сообщение текстом:")
        bot.register_next_step_handler(message, add_feedback, bot)
        return

    exec_query(f"insert into feedbacks (feedback) values ('{message.text}')")
    bot.send_message(config.MONITOR_CHAT_ID, "Новый отзыв:\n\n" + message.text)
    bot.send_message(message.chat.id, "Записал")

def show_feedbacks(message, bot):
    if message.text is None:
        bot.send_message(message.chat.id, "Отправь, пожалуйста, сообщение текстом:")
        bot.register_next_step_handler(message, show_feedbacks, bot)
        return 
    
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

