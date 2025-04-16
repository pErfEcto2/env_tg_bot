import config
import telebot
import sqlite3 
import requests
import urllib.parse


int_in_emojies = {str(i): f"{i}\uFE0F\u20E3 " for i in range(10)}

def exec_query(query: str):
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

    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Окей", reply_markup=keyboard_after)
        return

    buildings = list(map(lambda x: x[0], exec_query("select address from buildings")))
    
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

def addr_to_coords(address):
    rows = exec_query(f"""select lat, lon, address from plastic where address = '{address}' union\
                              select lat, lon, address from metall where address = '{address}' union\
                              select lat, lon, address from caps where address = '{address}' union\
                              select lat, lon, address from battaries where address = '{address}'""")

    for row in rows:
        if all(row[:2]):
            return [float(row[0]), float(row[1])]

    try:
        encoded_address = urllib.parse.quote(address)
        resp = requests.get(f"https://geocode-maps.yandex.ru/v1/?apikey={config.YANDEX_API_KEY}&geocode={encoded_address}&format=json")
        if resp.status_code != 200:
            return [0, 0]

        data = resp.json()
        lon, lat = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
        lat, lon = float(lat), float(lon)

        exec_query(f"update plastic set lat = {lat}, lon = {lon} where address = '{address}';")
        exec_query(f"update metall set lat = {lat}, lon = {lon} where address = '{address}';")
        exec_query(f"update caps set lat = {lat}, lon = {lon} where address = '{address}';")
        exec_query(f"update battaries set lat = {lat}, lon = {lon} where address = '{address}';")

        return [lat, lon]
    except Exception:
        return [0, 0]

def send_addresses(message_chat_id, bot, places):
    if not places:
        bot.send_message(message_chat_id, "К сожалению, ничего не найдено")
        return
    else:
        bot.send_message(message_chat_id, "Вот, что мне удалось найти:")
    
    for description, address in places:
        lat, lon = addr_to_coords(address)
        bot.send_message(message_chat_id, "Описание:\n" + description)

        if lat == 0 and lon == 0:
            bot.send_message(message_chat_id, "Адрес пункта:\n" + address)
            continue

        bot.send_location(message_chat_id, lat, lon)


