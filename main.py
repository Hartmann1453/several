import random
import defs, setting, classes as cl
import json, aiosqlite, time
from vkbottle.bot import Message
from vkbottle import GroupTypes, GroupEventType, Keyboard, KeyboardButtonColor, Text
from vkbottle.modules import json

# Отлавливаем новые сообщения
@setting.bot.on.chat_message()
async def message_handler(message: Message):

    user = cl.User(message.from_id)
    await user.load()

    mess_adm = message.text.split(' ')
    mess = message.text.lower()
    mess = mess.split(' ')
    count = message.text.count(' ')


    if mess[0] == 'пир':
        #
        await user.send_message(user.vk_id, f'{message.peer_id}')
    if mess[0] == 'кости':
        #
        await user.send_message(message.peer_id, f'Вам выпало: {random.randint(2, 12)}')
@setting.bot.on.private_message()
async def message_handler(message: Message):
    user = cl.User(message.from_id)
    await user.load()
    try:
        payload = json.loads(message.payload)
        payload = payload['payload']
    except: payload = 'None'
    print(f"___________________________________\nсообщение: {message.text}\nPayload: {payload}")

    mess_adm = message.text.split(' ')
    mess = message.text.lower()
    mess = mess.split(' ')
    count = message.text.count(' ')

    if payload == 'Начать':
        keyboard = Keyboard()
        keyboard.add(Text("Окраина", {"payload": "Окраина"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Информация", {"payload": "Инфо город"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Рынок", {"payload": "Рынок"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Таверна", {"payload": "Таверна"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Покинуть город", {"payload": "Покинуть город"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, "Вступительное сообщение. Вы в городе Хартмарк. Вот меню:", keyboard)
    if payload == 'Рынок':
        #
        await user.market_info()
    if payload == 'Инфо город':
        #
        await user.town_info()
    if payload == 'Покинуть город':
        #
        await user.exit()
    if payload == 'войти в город':
        #
        await user.inside()
    if payload == 'чек ресурсов':
        #
        await user.check_res()
    if payload == 'чек путей':
        #
        await user.see_loc()
    if payload == 'город':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Окраина", {"payload": "Окраина"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Информация", {"payload": "Инфо город"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Рынок", {"payload": "Рынок"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Таверна", {"payload": "Таверна"}), color=KeyboardButtonColor.PRIMARY)
        if user.bot_id == town[3]:
            keyboard.row()
            keyboard.add(Text("Дворец", {"payload": "Дворец"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Покинуть город", {"payload": "Покинуть город"}), color=KeyboardButtonColor.SECONDARY)

        await user.send_keyboard(user.vk_id, f"Вы вошли на центральную площадь города {user.location}.", keyboard)
    if payload == 'тав кости':
        keyboard = Keyboard()
        keyboard.add(Text("50 сер.", {"payload": "кости 50"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("250 сер.", {"payload": "кости 250"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("1000 сер.", {"payload": "кости 1000"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Вернутся", {"payload": "Таверна"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, "Вы подошли к игорному столу.\n На какую ставку будем играть?", keyboard)
    if payload == 'кости 50':
        pl_rand = random.randint(2, 12)
        cp_rand = random.randint(2, 12) + 1

        if user.cash < 50:
            await user.send_message(user.vk_id,"У вас нет столько серебра.")
            return

        if cp_rand > 12:
            cp_rand = 12

        if pl_rand > cp_rand:
            user.cash += 50
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()
            await user.send_message(user.vk_id, f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Вы выиграли 50 серебряных монет.")

        if pl_rand < cp_rand:
            user.cash -= 50
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()
            await user.send_message(user.vk_id, f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Вы проиграли 50 серебряных монет.")

        if pl_rand == cp_rand:
            await user.send_message(user.vk_id, f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Ничья.")
    if payload == 'кости 250':
        pl_rand = random.randint(2, 12)
        cp_rand = random.randint(2, 12) + 1

        if user.cash < 250:
            await user.send_message(user.vk_id,"У вас нет столько серебра.")
            return

        if cp_rand > 12:
            cp_rand = 12

        if pl_rand > cp_rand:
            user.cash += 250
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()
            await user.send_message(user.vk_id,f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Вы выиграли 250 серебряных монет.")

        if pl_rand < cp_rand:
            user.cash -= 250
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()
            await user.send_message(user.vk_id,f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Вы проиграли 250 серебряных монет.")

        if pl_rand == cp_rand:
            await user.send_message(user.vk_id,f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Ничья.")
    if payload == 'кости 1000':
        pl_rand = random.randint(2, 12)
        cp_rand = random.randint(2, 12) + 1

        if user.cash < 1000:
            await user.send_message(user.vk_id,"У вас нет столько серебра.")
            return

        if cp_rand > 12:
            cp_rand = 12

        if pl_rand > cp_rand:
            user.cash += 1000
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()
            await user.send_message(user.vk_id,f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Вы выиграли 1000 серебряных монет.")

        if pl_rand < cp_rand:
            user.cash -= 1000
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()
            await user.send_message(user.vk_id,f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Вы проиграли 1000 серебряных монет.")

        if pl_rand == cp_rand:
            await user.send_message(user.vk_id,f"Вы выкинули {pl_rand}, соперник же {cp_rand}\n"
                                                "Ничья.")

    if payload == 'Таверна':
        keyboard = Keyboard()
        keyboard.add(Text("Сыграть в кости", {"payload": "тав кости"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Командир наёмников", {"payload": "наёмники"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Вернутся", {"payload": "город"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, "Вы вошли в таверну.", keyboard)
    if payload == 'наёмники':
        hire = json.loads(user.hire)
        price = {}
        price['наемный стрелок'] = setting.price['наемный стрелок']['серебро']
        price['наемный всадник'] = setting.price['наемный всадник']['серебро']
        price['наемный воин'] = setting.price['наемный воин']['серебро']
        price = hire[user.location]['наемный стрелок'] * price['наемный стрелок'] + hire[user.location]['наемный всадник'] * price['наемный всадник'] + hire[user.location]['наемный воин'] * price['наемный воин']

        keyboard = Keyboard()
        keyboard.add(Text("По рукам", {"payload": "нанять"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Вернутся", {"payload": "Таверна"}), color=KeyboardButtonColor.SECONDARY)


        await user.send_keyboard(user.vk_id, f"Вы подошли к командиру наёмников.\nИз доступных сейчас бойцов есть:\nСтрелки:{hire[user.location]['наемный стрелок']}\nВсадники:{hire[user.location]['наемный всадник']}\nВоины:{hire[user.location]['наемный воин']}\n Стоимость всех солдат: {price}", keyboard)

    if payload == 'нанять':
        hire = json.loads(user.hire)
        price = {}
        price['наемный стрелок'] = setting.price['наемный стрелок']['серебро']
        price['наемный всадник'] = setting.price['наемный всадник']['серебро']
        price['наемный воин'] = setting.price['наемный воин']['серебро']
        price = hire[user.location]['наемный стрелок'] * price['наемный стрелок'] + hire[user.location]['наемный всадник'] * price['наемный всадник'] + hire[user.location]['наемный воин'] * price['наемный воин']

        if user.cash < price:
            await user.send_message(user.vk_id, f"У вас недостаточно серебра.")
            return

        army = json.loads(user.army)
        army['наемный стрелок'] += hire[user.location]['наемный стрелок']
        army['наемный всадник'] += hire[user.location]['наемный всадник']
        army['наемный воин'] += hire[user.location]['наемный воин']

        await user.send_message(user.vk_id, f"Вы наняли:\n"
                                             f"{hire[user.location]['наемный стрелок']} стрелков\n"
                                             f"{hire[user.location]['наемный всадник']} всадников\n"
                                             f"{hire[user.location]['наемный воин']} воинов\n"
                                             f"Общие затраты составили: {price}")

        hire[user.location]['наемный стрелок'] = 0
        hire[user.location]['наемный всадник'] = 0
        hire[user.location]['наемный воин'] = 0

        user.cash -= price
        hire = json.dumps(hire, ensure_ascii=False)
        army = json.dumps(army, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = {user.cash}, army = '{army}', hire = '{hire}' WHERE vk_id = {user.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

    if payload == 'Окраина':
        #
        await user.pretown()
    if payload == 'Сбор':
        #
        await user.harvest()
    if payload == 'Инфо окраины':
        #
        await user.check_biz()
    if payload == 'бизнес':
        town = cl.Town(user.location)
        await town.load()
        await town.create_biz(user.bot_id, message.text)
    if payload == 'В провинцию':
        keyboard = Keyboard()
        keyboard.add(Text("Осмотреться", {"payload": "чек ресурсов"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Дороги", {"payload": "чек путей"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Собирать", {"payload": "собирательство"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Искать поселение", {"payload": "войти в город"}), color=KeyboardButtonColor.SECONDARY)

        reg = defs.replace_name(user.location)

        await user.send_keyboard(user.vk_id, f"Вы вышли в {reg}.", keyboard)
    if payload[:-1] == 'Путь':
        number = int(payload[-1])
        await user.travel(number)
        keyboard = Keyboard()
        keyboard.add(Text("Оглянуться", {"payload": "Путешествие"}), color=KeyboardButtonColor.PRIMARY)
        await user.send_keyboard(user.vk_id, "Вы отправились в путь.", keyboard)


    if payload == 'собирательство':
        #
        await user.start_work()
    if payload == 'фарм камня':
        #
        await user.mine_stone()
    if payload == 'фарм дерева':
        #
        await user.mine_tree()
    if payload == 'фарм руды':
        #
        await user.mine_ore()
    if payload == 'фарм хлопка':
        #
        await user.mine_silk()
    if payload == 'фарм рыбы':
        #
        await user.fishing()
    if payload == 'продажа ресов':
        keyboard = Keyboard()
        keyboard.add(Text("Камень", {"payload": "продажа камня"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Дерево", {"payload": "продажа дерева"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Руду", {"payload": "продажа руды"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Хлопок", {"payload": "продажа хлопка"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Рыбу", {"payload": "продажа рыбы"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": "город"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, "Какой ресурс вы хотите продать?", keyboard)
    if payload == 'покупка ресов':
        keyboard = Keyboard()
        keyboard.add(Text("Камень", {"payload": "покупка камня"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Дерево", {"payload": "покупка дерева"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Руду", {"payload": "покупка руды"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Хлопок", {"payload": "покупка хлопка"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Рыбу", {"payload": "покупка рыбы"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": "город"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, "Какой ресурс вы хотите купить?", keyboard)
    if payload == 'Инструменты':
        #
        await user.send_message(user.vk_id,"В разработке")

    if payload == 'продажа камня':
        #
        await user.sell_stone()
    if payload == 'продажа дерева':
        #
        await user.sell_tree()
    if payload == 'продажа руды':
        #
        await user.sell_ore()
    if payload == 'продажа хлопка':
        #
        await user.sell_silk()
    if payload == 'продажа рыбы':
        #
        await user.sell_fish()

    if payload == 'покупка камня':
        #
        await user.buy_stone()
    if payload == 'покупка дерева':
        #
        await user.buy_tree()
    if payload == 'покупка руды':
        #
        await user.buy_ore()
    if payload == 'покупка хлопка':
        #
        await user.buy_silk()
    if payload == 'покупка рыбы':
        #
        await user.buy_fish()

    if payload == "Дворец":
        user.status = 'Нет'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Налоги", {"payload": "Дворец|Налоги"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Армия", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Собрать налоги", {"payload": "Дворец|Сбор налогов"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Вернуться в город", {"payload": "город"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f"Вы во дворце города {user.location}, повелитель.\nЧто прикажете?", keyboard)

    if payload == "Дворец|Сбор налогов":

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        inventar = json.loads(user.inventar)
        obrok = json.loads(town[11])

        inventar['рыба'] += obrok['рыба']
        inventar['камень'] += obrok['камень']
        inventar['дерево'] += obrok['дерево']
        inventar['руда'] += obrok['руда']
        inventar['хлопок'] += obrok['хлопок']
        user.cash += obrok['налог']


        await user.send_message(user.vk_id, f"Вы собрали подати с города {user.location}:\n"
                                            f"Рыба: {obrok['рыба']}\n"
                                            f"Камень: {obrok['камень']}\n"
                                            f"Дерево: {obrok['дерево']}\n"
                                            f"Руда: {obrok['руда']}\n"
                                            f"Хлопок: {obrok['хлопок']}\n"
                                            f"Серебро: {obrok['налог']}\n")

        obrok['рыба'] = 0
        obrok['камень'] = 0
        obrok['дерево'] = 0
        obrok['руда'] = 0
        obrok['хлопок'] = 0
        obrok['налог'] = 0

        obrok = json.dumps(obrok, ensure_ascii=False)
        inventar = json.dumps(inventar, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = {user.cash}, inventar = '{inventar}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET obrok = '{obrok}' WHERE name = '{user.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

    if payload == "Дворец|Налоги":
        user.status = 'Нет'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Оброк", {"payload": "Дворец|Налоги|Оброк"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Земельный налог", {"payload": "Дворец|Налоги|Земельный налог"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Подушная подать", {"payload": "Дворец|Налоги|Подушная подать"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": "Дворец"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f"Нынешние налоги, повелитель:\n"
                                             f"Оброк: {town[7]}%\n"
                                             f"Земельный налог: {town[6]} серебряных монет.\n"
                                             f"Подушная подать: {town[5]} серебряных монет.\n"
                                             f"\n"
                                             f"Какой из них Вы желаете изменить?",
                                     keyboard)
    if payload == 'Дворец|Налоги|Оброк':
        user.status = 'Оброк'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Налоги"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Ваша воля, повелитель.\nКакой процент благ мы теперь будем брать с граждан?', keyboard)
    if payload == 'Дворец|Налоги|Подушная подать':
        user.status = 'Подушная подать'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Налоги"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Ваша воля, повелитель.\nСколько монет мы теперь будем брать с крестьян?', keyboard)
    if payload == 'Дворец|Налоги|Земельный налог':
        user.status = 'Земельный налог'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Налоги"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Ваша воля, повелитель.\nКакой земельный налог мы теперь будем взымать с купцов?', keyboard)

    if payload == "Дворец|Армия":
        user.status = 'Нет'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        garnizon = json.loads(town[9])

        keyboard = Keyboard()
        keyboard.add(Text("Рекрутский сбор", {"payload": "Дворец|Армия|Рекрут"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Обучение войск", {"payload": "Дворец|Армия|Обучение"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Обмен войсками", {"payload": "Дворец|Армия|Гарнизон"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": "Дворец"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f"Гарнизон города {user.location}, повелитель:\n"
                                             f"Рекруты: {garnizon['рекруты']}\n"
                                             f"Ополчение: {garnizon['ополченец']}\n"
                                             f"Воины: {garnizon['воин']}\n"
                                             f"Стрелки: {garnizon['стрелок']}\n"
                                             f"Всадники: {garnizon['всадник']}\n"
                                             f"Наемные воины: {garnizon['наемный воин']}\n"
                                             f"Наемные стрелки: {garnizon['наемный стрелок']}\n"
                                             f"Наемные всадники: {garnizon['наемный всадник']}\n"
                                             f"\n"
                                             f"Рекрусткий сбор {town[8]} человек на каждые сто душ.\n"
                                             f"Что Вы намереваетесь сделать?",
                                     keyboard)
    if payload == 'Дворец|Армия|Рекрут':
        user.status = 'Рекрут'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Ваша воля, повелитель.\nКакой процент граждан мы теперь будем рекрутировать?', keyboard)
    if payload == "Дворец|Армия|Обучение":
        user.status = 'Нет'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Воины", {"payload": "Дворец|Армия|Обучение|Воин"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Всадники", {"payload": "Дворец|Армия|Обучение|Всадник"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Стрелки", {"payload": "Дворец|Армия|Обучение|Стрелок"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Собрать ополчение", {"payload": "Дворец|Армия|Обучение|Ополчение"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f"Кого Вы хотели бы обучить, повелитель?",
                                 keyboard)
    if payload == 'Дворец|Армия|Обучение|Воин':
        user.status = 'Воин'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f'Стата и цена воина', keyboard)
    if payload == 'Дворец|Армия|Обучение|Стрелок':
        user.status = 'Стрелок'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Стата и цена Стрелок', keyboard)
    if payload == 'Дворец|Армия|Обучение|Всадник':
        user.status = 'Всадник'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Стата и цена Всадник', keyboard)
    if payload == 'Дворец|Армия|Обучение|Ополчение':
        user.status = 'Ополченец'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец|Армия"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id,
                                f'Стата и цена Ополченец', keyboard)
    if payload == "Дворец|Армия|Гарнизон":
        user.status = 'Гарнизон'
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET status = '{user.status}' WHERE bot_id = {user.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        garnizon = json.loads(town[9])

        keyboard = Keyboard()
        keyboard.add(Text("Назад", {"payload": "Дворец"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f"Гарнизон города {user.location}, повелитель:\n"
                                             f"1.Рекруты: {garnizon['рекруты']}\n"
                                             f"2.Ополчение: {garnizon['ополченец']}\n"
                                             f"3.Воины: {garnizon['воин']}\n"
                                             f"4.Стрелки: {garnizon['стрелок']}\n"
                                             f"5.Всадники: {garnizon['всадник']}\n"
                                             f"6.Наемные воины: {garnizon['наемный воин']}\n"
                                             f"7.Наемные стрелки: {garnizon['наемный стрелок']}\n"
                                             f"8.Наемные всадники: {garnizon['наемный всадник']}\n"
                                             f"\n"
                                             f"Взять войска из гарнизона \"Забрать [№ Юнита] [Количество]\"\n"
                                             f"Оставить войска в гарнизоне \"Отдать [№ Юнита] [Количество]\"",
                                     keyboard)

    if payload == 'Знамена|Выйти':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        type_loc = await defs.type_of_loc(flag[4])

        user.location = flag[4]

        if flag[6] == 'Марш':
            await user.send_message(user.vk_id, "Вы не можете покинуть знамя пока оно на марше.")
            return

        if type_loc == 'Town':
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            keyboard = Keyboard()
            keyboard.add(Text("Окраина", {"payload": "Окраина"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Информация", {"payload": "Инфо город"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Рынок", {"payload": "Рынок"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Таверна", {"payload": "Таверна"}), color=KeyboardButtonColor.PRIMARY)
            if user.bot_id == town[3]:
                keyboard.row()
                keyboard.add(Text("Дворец", {"payload": "Дворец"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Покинуть город", {"payload": "Покинуть город"}), color=KeyboardButtonColor.SECONDARY)

            await user.send_keyboard(user.vk_id, f"Вы вышли на центральную площадь города {user.location}.", keyboard)

        if type_loc == 'Region':

            user.location = flag[4]
            reg = defs.replace_name(flag[4])

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET location = '{user.location}' WHERE vk_id = {user.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()

            keyboard = Keyboard()
            keyboard.add(Text("Осмотреться", {"payload": "чек ресурсов"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Дороги", {"payload": "чек путей"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Собирать", {"payload": "собирательство"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Искать поселение", {"payload": "войти в город"}), color=KeyboardButtonColor.SECONDARY)

            await user.send_keyboard(user.vk_id, f"Вы вышли в {reg}.", keyboard)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"DELETE FROM Flags WHERE name = '{user.name}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET location = '{user.location}' WHERE vk_id = {user.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()
    if payload == 'Знамена|Открыть набор':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Flags SET open = 'Открыт' WHERE comander = {flag[5]} and flag_id = '{flag[3]}'")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Закрыть набор", {"payload": f"Знамена|Закрыть набор"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}), color=KeyboardButtonColor.SECONDARY)

        await user.send_keyboard(user.vk_id, "Набор в ваше знамя открыт.", keyboard)
    if payload == 'Знамена|Закрыть набор':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Flags SET open = 'Закрыт' WHERE comander = {flag[5]} and flag_id = '{flag[3]}'")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Открыть набор", {"payload": f"Знамена|Открыть набор"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}), color=KeyboardButtonColor.SECONDARY)

        await user.send_keyboard(user.vk_id, "Набор в ваше знамя открыт.", keyboard)
    if payload == 'Знамена':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        if flag[7] == 'Закрыт':
            keyboard = Keyboard()
            keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Открыть набор", {"payload": f"Знамена|Открыть набор"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}), color=KeyboardButtonColor.SECONDARY)

        if flag[7] == 'Открыт':
            keyboard = Keyboard()
            keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Закрыть набор", {"payload": f"Знамена|Закрыть набор"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}), color=KeyboardButtonColor.SECONDARY)

        await user.send_keyboard(user.vk_id, "Вы вернулись к знаменам", keyboard)
    if payload == 'Знамена|Пути':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        if flag[5] != user.bot_id:
            await user.send_message(user.vk_id, "Вы не командир знамени.")
            return

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{flag[4]}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        roads = json.loads(result[1])
        i = 0
        keyboard = Keyboard()
        for road in roads.keys():
            i += 1
            road_rep = defs.replace_name(road)
            keyboard.add(Text(road_rep, {"payload": f"Знамена|Путь{i}"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": f"Знамена"}), color=KeyboardButtonColor.SECONDARY)
        await user.send_keyboard(user.vk_id, f"Куда направляемся, милорд?", keyboard)
    if payload[:-1] == 'Знамена|Путь':
        number = int(payload[-1])

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{flag[4]}'")
        region = await command.fetchone()
        await command.close()
        await connection.close()

        roads = json.loads(region[1])
        i = 0
        for road in roads.keys():
            i += 1

            if i == number:

                json_res = {
                    'flag_id': flag[3],
                    'target loc': road
                }
                json_res = json.dumps(json_res, ensure_ascii=False)
                data_time = round(int(roads[f'{road}']) / 10)
                await defs.create_task('Марш', json_res, data_time)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Flags SET status = 'Марш' WHERE flag_id = {flag[3]}")
        await connection.commit()
        await command.close()
        await connection.close()

        await user.send_message(user.vk_id, "Знамёна встали на марш, вскоре мы прибудем на место, милорд.")
    if payload == 'Знамена|Разведка':
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE location = '{flag[4]}'")
        flags_in_reg = await command.fetchall()
        await command.close()
        await connection.close()

        arr_ids = {}
        ids = {}
        for flag_in_reg in flags_in_reg:
            print(f'{flag_in_reg} in {flags_in_reg}')
            arr_ids[flag_in_reg[3]] = 'Существует'
        i = 0
        for arr_id in arr_ids.keys():
            if flag[3] != arr_id:
                i += 1
                ids[i] = arr_id
        txt = f"Вы провели разведку в {defs.replace_name(flag[4])}.\n" \
              f"Обнаруженные знамёна:\n\n"


        for id in ids:
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = {id}")
            flagid = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {flagid[5]}")
            flag_com = await command.fetchone()
            await command.close()
            await connection.close()

            txt += f"Знамя №{id}, во главе с {flag_com[1]}.\n"

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{flag[4]}'")
        region = await command.fetchone()
        await command.close()
        await connection.close()

        if region[2] != 'Нет':
            txt += f"\nТак же вдали видны знамена города {region[2]}!"

        await user.send_message(user.vk_id, txt)
    if payload == 'Знамена|Информация':

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
        flag = await command.fetchone()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = {flag[3]}")
        unity_flags = await command.fetchall()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {flag[5]}")
        commander = await command.fetchone()
        await command.close()
        await connection.close()

        union_army = {
            "рекруты": 0,
            "ополченец": 0,
            "стрелок": 0,
            "всадник": 0,
            "воин": 0,
            "наемный стрелок": 0,
            "наемный всадник": 0,
            "наемный воин": 0
        }

        for unity_flag in unity_flags:
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {unity_flag[2]}")
            unit_user = await command.fetchone()
            await command.close()
            await connection.close()

            army = json.loads(unit_user[5])

            for key, value in army.items():
                union_army[key] += value

        txt = f"Информация о знамени №{flag[3]}:\n" \
              f"Локация: {flag[4]}.\n" \
              f"Командующий: {commander[1]}.\n" \
              f"Армия:\n\n"

        for key, value in union_army.items():
            txt += f'{key}: {value}\n'

        await user.send_message(user.vk_id, txt)
    if payload == 'Работа|Чек':
        #
        await user.send_message(user.vk_id,"Вы заняты до конца дня.")
    if payload == 'Путешествие':
        #
        await user.send_message(user.vk_id,"Вы в пути до конца дня, наслаждайтесь.")

    if count == 0:
        if user.status == 'Подушная подать':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] > 100 or mess[0] < 0:
                        await user.send_message(user.vk_id, "Мы не можем выставить налог от 0 до 100.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(
                        f"UPDATE Towns SET tax_pop = {mess[0]} WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                    await user.send_message(user.vk_id, f"Отныне подушный налог составляет {mess[0]} монет на душу населения.")

                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return
        if user.status == 'Земельный налог':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] > 10000 or mess[0] < 0:
                        await user.send_message(user.vk_id, "Мы можем выставить налог от 0 до 10000.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(
                        f"UPDATE Towns SET tax_land = {mess[0]} WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                    await user.send_message(user.vk_id, f"Отныне земельный налог составляет {mess[0]} монет за земельный участок.")

                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return
        if user.status == 'Оброк':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] > 100 or mess[0] < 0:
                        await user.send_message(user.vk_id, "Мы можем выставить налог от 0 до 100.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(
                        f"UPDATE Towns SET tax_reg = {mess[0]} WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                    await user.send_message(user.vk_id, f"Отныне оброк составляет {mess[0]}%  от собранных благ.")

                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return
        if user.status == 'Рекрут':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] > 100 or mess[0] < 0:
                        await user.send_message(user.vk_id, "Мы можем выставить сбор от 0 до 100.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(
                        f"UPDATE Towns SET tax_recruit = {mess[0]} WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                    await user.send_message(user.vk_id, f"Отныне рекрутский набор составляет {mess[0]} человек на сотню душ.")

                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return
        if user.status == 'Воин' and payload == 'None':
            if mess[0] != 'назад':
                #try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] < 0:
                        await user.send_message(user.vk_id, "нужно ввести положительное число.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
                    town = await command.fetchone()
                    await command.close()
                    await connection.close()

                    garnizon = json.loads(town[9])

                    if mess[0] > garnizon['рекруты']:
                        await user.send_message(user.vk_id, "В гарнизоне нет столько рекрутов, повелитель.")
                        return

                    market = json.loads(town[4])
                    price = {}
                    price['руда'] = setting.price['воин']['руда'] * mess[0]
                    price['хлопок'] = setting.price['воин']['хлопок'] * mess[0]
                    price['обучение'] = setting.price['воин']['серебро'] * mess[0]
                    if market['Склад']['руда'] < price['руда']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно руды. [Нужно {price['руда']}]")
                        return
                    if market['Склад']['хлопок'] < price['хлопок']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно хлопка. [Нужно {price['хлопок']}]")
                        return

                    price['общая'] = price['обучение'] + price['руда'] * market['Цена']['руда'] + price['хлопок'] * market['Цена']['хлопок']

                    if user.cash < price['общая']:
                        await user.send_message(user.vk_id, f"У вас не хватает денег. [Общая стоимость: {price['общая']}]")
                        return


                    # ________
                    market['Склад']['руда'] -= price['руда']
                    market['Склад']['хлопок'] -= price['хлопок']
                    user.cash -= price['общая']
                    garnizon['рекруты'] -= mess[0]

                    js_task = {
                        "vk_id": user.vk_id,
                        "тип солдат": "воин",
                        "количество солдат": mess[0],
                        "город": user.location
                    }

                    js_task = json.dumps(js_task, ensure_ascii=False)

                    data = 90
                    await defs.create_task('Обучение солдат', js_task, data)

                    # _______


                    await user.send_message(user.vk_id, f"Мы начали обучать {mess[0]} воинов, потратив на это:\n{price['общая']} серебра.\n{price['руда']} ед. руды с рынка.\n{price['хлопок']} ед. хлопка с рынка.\nОбучение будет завершено через {data} дней.")

                    garnizon = json.dumps(garnizon, ensure_ascii=False)
                    market = json.dumps(market, ensure_ascii=False)

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE bot_id = {user.bot_id}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Towns SET market = '{market}', garnizon = '{garnizon}' WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                #except:
                #    await user.send_message(user.vk_id, "Необходимо ввести число.")
                #    return
        if user.status == 'Стрелок' and payload == 'None':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] < 0:
                        await user.send_message(user.vk_id, "нужно ввести положительное число.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
                    town = await command.fetchone()
                    await command.close()
                    await connection.close()

                    garnizon = json.loads(town[9])

                    if mess[0] > garnizon['рекруты']:
                        await user.send_message(user.vk_id, "В гарнизоне нет столько рекрутов, повелитель.")
                        return

                    market = json.loads(town[4])
                    price = {}
                    price['дерево'] = setting.price['стрелок']['дерево'] * mess[0]
                    price['хлопок'] = setting.price['стрелок']['хлопок'] * mess[0]
                    price['обучение'] = setting.price['стрелок']['серебро'] * mess[0]
                    if market['Склад']['дерево'] < price['дерево']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно дерева. [Нужно {price['дерево']}]")
                        return
                    if market['Склад']['хлопок'] < price['хлопок']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно хлопка. [Нужно {price['хлопок']}]")
                        return

                    price['общая'] = price['обучение'] + price['дерево'] * market['Цена']['дерево'] + price['хлопок'] * market['Цена']['хлопок']

                    if user.cash < price['общая']:
                        await user.send_message(user.vk_id, f"У вас не хватает денег. [Общая стоимость: {price['общая']}]")
                        return

                    market['Склад']['дерево'] -= price['дерево']
                    market['Склад']['хлопок'] -= price['хлопок']
                    user.cash -= price['общая']
                    garnizon['рекруты'] -= mess[0]


                    js_task = {
                        "vk_id": user.vk_id,
                        "тип солдат": "стрелок",
                        "количество солдат": mess[0],
                        "город": user.location
                    }

                    js_task = json.dumps(js_task, ensure_ascii=False)

                    data = 90
                    await defs.create_task('Обучение солдат', js_task, data)

                    await user.send_message(user.vk_id, f"Мы начали обучать {mess[0]} стрелков, потратив на это:\n{price['общая']} серебра.\n{price['дерево']} ед. дерева с рынка.\n{price['хлопок']} ед. хлопка с рынка.")

                    garnizon = json.dumps(garnizon, ensure_ascii=False)
                    market = json.dumps(market, ensure_ascii=False)

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE bot_id = {user.bot_id}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Towns SET market = '{market}', garnizon = '{garnizon}' WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return
        if user.status == 'Всадник' and payload == 'None':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] < 0:
                        await user.send_message(user.vk_id, "нужно ввести положительное число.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
                    town = await command.fetchone()
                    await command.close()
                    await connection.close()

                    garnizon = json.loads(town[9])

                    if mess[0] > garnizon['рекруты']:
                        await user.send_message(user.vk_id, "В гарнизоне нет столько рекрутов, повелитель.")
                        return

                    market = json.loads(town[4])
                    price = {}
                    price['руда'] = setting.price['всадник']['руда'] * mess[0]
                    price['дерево'] = setting.price['всадник']['дерево'] * mess[0]
                    price['хлопок'] = setting.price['всадник']['хлопок'] * mess[0]
                    price['обучение'] = setting.price['всадник']['серебро'] * mess[0]

                    if market['Склад']['руда'] < price['руда']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно руды. [Нужно {price['руда']}]")
                        return
                    if market['Склад']['хлопок'] < price['хлопок']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно хлопка. [Нужно {price['хлопок']}]")
                        return
                    if market['Склад']['дерево'] < price['дерево']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно дерева. [Нужно {price['дерево']}]")
                        return

                    price['общая'] = price['обучение'] + price['руда'] * market['Цена']['руда'] + price['дерево'] * market['Цена']['дерево'] + price['хлопок'] * market['Цена']['хлопок']

                    if user.cash < price['общая']:
                        await user.send_message(user.vk_id, f"У вас не хватает денег. [Общая стоимость: {price['общая']}]")
                        return

                    market['Склад']['руда'] -= price['руда']
                    market['Склад']['хлопок'] -= price['хлопок']
                    market['Склад']['дерево'] -= price['дерево']
                    user.cash -= price['общая']
                    garnizon['рекруты'] -= mess[0]


                    js_task = {
                        "vk_id": user.vk_id,
                        "тип солдат": "всадник",
                        "количество солдат": mess[0],
                        "город": user.location
                    }

                    js_task = json.dumps(js_task, ensure_ascii=False)

                    data = 90
                    await defs.create_task('Обучение солдат', js_task, data)

                    await user.send_message(user.vk_id, f"Мы начали обучать {mess[0]} всадников, потратив на это:\n{price['общая']} серебра.\n{price['руда']} ед. руды с рынка.\n{price['дерево']} ед. дерева с рынка.\n{price['хлопок']} ед. хлопка с рынка.")

                    garnizon = json.dumps(garnizon, ensure_ascii=False)
                    market = json.dumps(market, ensure_ascii=False)

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE bot_id = {user.bot_id}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Towns SET market = '{market}', garnizon = '{garnizon}' WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return
        if user.status == 'Ополченец' and payload == 'None':
            if mess[0] != 'назад':
                try:
                    mess[0] = round(int(mess[0]))
                    if mess[0] < 0:
                        await user.send_message(user.vk_id, "нужно ввести положительное число.")
                        return

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
                    town = await command.fetchone()
                    await command.close()
                    await connection.close()

                    garnizon = json.loads(town[9])

                    if mess[0] > garnizon['рекруты']:
                        await user.send_message(user.vk_id, "В гарнизоне нет столько рекрутов, повелитель.")
                        return

                    market = json.loads(town[4])
                    price = {}
                    price['дерево'] = setting.price['ополченец']['дерево'] * mess[0]
                    price['обучение'] = setting.price['ополченец']['серебро'] * mess[0]
                    if market['Склад']['дерево'] < price['дерево']:
                        await user.send_message(user.vk_id, f"На рынке города недостаточно дерева. [Нужно {price['дерево']}]")
                        return

                    price['общая'] = price['обучение'] + price['дерево'] * market['Цена']['дерево']

                    if user.cash < price['общая']:
                        await user.send_message(user.vk_id, f"У вас не хватает денег. [Общая стоимость: {price['общая']}]")
                        return

                    market['Склад']['дерево'] -= price['дерево']
                    user.cash -= price['общая']
                    garnizon['рекруты'] -= mess[0]
                    garnizon['ополченец'] += mess[0]

                    await user.send_message(user.vk_id, f"Мы собрали {mess[0]} ополчения, потратив на это:\n{price['общая']} серебра.\n{price['дерево']} ед. дерева с рынка.\n")

                    garnizon = json.dumps(garnizon, ensure_ascii=False)
                    market = json.dumps(market, ensure_ascii=False)

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Users SET cash = {user.cash} WHERE bot_id = {user.bot_id}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Towns SET market = '{market}', garnizon = '{garnizon}' WHERE name = '{user.location}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()
                except:
                    await user.send_message(user.vk_id, "Необходимо ввести число.")
                    return

        if mess[0] == 'паспорт':
            #
            await user.passport()
        if mess[0] == 'инвентарь':
            #
            await user.check_inventar()
        if mess[0] == 'армия' and payload == 'None':
            #
            await user.check_army()
        if mess[0] == 'пир':
            #
            await user.send_message(user.vk_id, f'{message.peer_id}')

    if count == 1:
        if mess[0] == 'создать' and mess[1] == 'знамя':

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            print(result)
            if result != None:
                await user.send_message(user.vk_id, f"Вы уже в составе знамени №{result[3]}")
                return

            type_loc = await defs.type_of_loc(user.location)

            if type_loc != 'Region':
                await user.send_message(user.vk_id, f"Созывать знамя можно только в регионе.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT MAX(flag_id) FROM Flags")
            result = await command.fetchone()
            await command.close()
            await connection.close()
            flag_id = result[0] + 1

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT MAX(id) FROM Flags")
            result = await command.fetchone()
            await command.close()
            await connection.close()
            id = result[0] + 1

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute("INSERT INTO Flags VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, user.name, user.bot_id, flag_id, user.location, user.bot_id, 'Привал', 'Закрыт'))
            await connection.commit()
            await command.close()

            keyboard = Keyboard()
            keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Открыть набор", {"payload": f"Знамена|Открыть набор"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}), color=KeyboardButtonColor.SECONDARY)

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET location = 'Знамя №{flag_id}' WHERE bot_id = {user.bot_id}")
            await connection.commit()
            await command.close()
            await connection.close()

            await user.send_keyboard(user.vk_id, f"[{flag_id}]Вы созвали знамёна.\n", keyboard)

    if count == 2:

        if user.status == 'Гарнизон' and payload == 'None':
            if mess[0] == 'забрать':
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
                town = await command.fetchone()
                await command.close()
                await connection.close()

                garnizon = json.loads(town[9])
                army = json.loads(user.army)

                try:
                    mess[1] = int(mess[1])
                except:
                    await user.send_message(user.vk_id, "Вторым аргументов нужно указать число")
                    return

                try:
                    mess[2] = int(mess[2])
                except:
                    await user.send_message(user.vk_id, "Третий аргумент должен быть числом")
                    return

                if mess[2] <= 0:
                    await user.send_message(user.vk_id, "Количество должно быть больше 0")
                    return

                if mess[1] == 1:
                    unit_type = 'рекруты'
                elif mess[1] == 2:
                    unit_type = 'ополченец'
                elif mess[1] == 3:
                    unit_type = 'воин'
                elif mess[1] == 4:
                    unit_type = 'стрелок'
                elif mess[1] == 5:
                    unit_type = 'всадник'
                elif mess[1] == 6:
                    unit_type = 'наемный воин'
                elif mess[1] == 7:
                    unit_type = 'наемный стрелок'
                elif mess[1] == 8:
                    unit_type = 'наемный всадник'
                else:
                    await user.send_message(user.vk_id, "Нужно выбрать тип войск от 1 до 8.")
                    return

                if garnizon[unit_type] < mess[2]:
                    await user.send_message(user.vk_id, "У вас нет столько солдат такого типа в гарнизоне.")
                    return

                garnizon[unit_type] -= mess[2]
                army[unit_type] += mess[2]

                await user.send_message(user.vk_id, f"Вы забрали {mess[2]} солдат из гарнизона.")

                army = json.dumps(army, ensure_ascii=False)
                garnizon = json.dumps(garnizon, ensure_ascii=False)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Towns SET garnizon = '{garnizon}' WHERE name = '{user.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Users SET army = '{army}' WHERE bot_id = {user.bot_id}")
                await connection.commit()
                await command.close()
                await connection.close()
            if mess[0] == 'отдать':
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{user.location}'")
                town = await command.fetchone()
                await command.close()
                await connection.close()

                garnizon = json.loads(town[9])
                army = json.loads(user.army)

                try:
                    mess[1] = int(mess[1])
                except:
                    await user.send_message(user.vk_id, "Вторым аргументов нужно указать число")
                    return

                try:
                    mess[2] = int(mess[2])
                except:
                    await user.send_message(user.vk_id, "Третий аргумент должен быть числом")
                    return

                if mess[2] <= 0:
                    await user.send_message(user.vk_id, "Количество должно быть больше 0")
                    return

                if mess[1] == 1:
                    unit_type = 'рекруты'
                elif mess[1] == 2:
                    unit_type = 'ополченец'
                elif mess[1] == 3:
                    unit_type = 'воин'
                elif mess[1] == 4:
                    unit_type = 'стрелок'
                elif mess[1] == 5:
                    unit_type = 'всадник'
                elif mess[1] == 6:
                    unit_type = 'наемный воин'
                elif mess[1] == 7:
                    unit_type = 'наемный стрелок'
                elif mess[1] == 8:
                    unit_type = 'наемный всадник'
                else:
                    await user.send_message(user.vk_id, "Нужно выбрать тип войск от 1 до 8.")
                    return

                if army[unit_type] < mess[2]:
                    await user.send_message(user.vk_id, "У вас нет столько солдат такого типа.")
                    return

                garnizon[unit_type] += mess[2]
                army[unit_type] -= mess[2]

                await user.send_message(user.vk_id, f"Вы отдали {mess[2]} солдат в гарнизон.")

                army = json.dumps(army, ensure_ascii=False)
                garnizon = json.dumps(garnizon, ensure_ascii=False)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Towns SET garnizon = '{garnizon}' WHERE name = '{user.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Users SET army = '{army}' WHERE bot_id = {user.bot_id}")
                await connection.commit()
                await command.close()
                await connection.close()

        if mess[0] == 'напасть' and mess[1] == 'на' and mess[2] == 'город':

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
            flag = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{flag[4]}'")
            region = await command.fetchone()
            await command.close()
            await connection.close()

            if region[2] == 'Нет':
                await user.send_message(user.vk_id, "В этой провинции нет города.")
                return

            if flag[5] != user.bot_id:
                await user.send_message(user.vk_id, "Только командующий может отдать приказ об атаке.")
                return


            js_task = {
                "Номер знамени": flag[3]
            }
            js_task = json.dumps(js_task, ensure_ascii=False)
            await defs.create_task('Сражение за город', js_task, 0)

            await user.send_message(user.vk_id, f"Вы начали бои за {region[2]}!")

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Flags SET status = 'В бою' WHERE flag_id = {flag[3]}")
            await connection.commit()
            await command.close()
            await connection.close()






        if mess[0] == 'передать':
            try:
                if user.cash >= int(mess[2]):
                    if int(mess[2]) > 0:
                        mess[2] = round(int(mess[2]), 0)
                        _user = cl.User(0)
                        await _user.load_bot_id(mess[1])
                        await user.Cash(-1 * mess[2])
                        await _user.Cash(mess[2])
                        await user.send_message(user.vk_id, f"Вы передали {mess[2]} монет игроку {_user.name}")
                        await user.send_message(_user.vk_id, f"{user.name} передал вам {mess[2]} монет.")
                    else: await user.send_message(user.vk_id,"Можно передать только положительное значение")
                else: await user.send_message(user.vk_id,"У вас нет столько монет")
            except:
                await user.send_message(user.vk_id,"Проверьте правильность команды. Передать [id игрока] [Сумма]")
    if count == 3:
        if mess[0] == 'встать' and mess[1] == 'под' and mess[2] == 'знамя':

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Flags WHERE name = '{user.name}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            print(result)
            if result != None:
                await user.send_message(user.vk_id, f"Вы уже в составе знамени №{result[3]}")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT MAX(id) FROM Flags")
            result = await command.fetchone()
            await command.close()
            await connection.close()
            id = result[0] + 1

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = '{mess[3]}'")
            flag = await command.fetchone()
            await command.close()
            await connection.close()

            if flag == None:
                await user.send_message(user.vk_id, f"Такого знамени не существует.")
                return

            if flag[4] != user.location:
                await user.send_message(user.vk_id, f"Чтобы присоединиться к знамени необходимо находиться с ним в одной локации.")
                return

            if flag[7] == 'Закрыт':
                await user.send_message(user.vk_id, f"Набор закрыт.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute("INSERT INTO Flags VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, user.name, user.bot_id, mess[3], flag[4], flag[5], flag[6], flag[7]))
            await connection.commit()
            await command.close()

            keyboard = Keyboard()
            keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}), color=KeyboardButtonColor.SECONDARY)

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"UPDATE Users SET location = 'Знамя №{mess[3]}' WHERE bot_id = {user.bot_id}")
            await connection.commit()
            await command.close()
            await connection.close()

            await user.send_keyboard(user.vk_id, f"Вы встали под знамя №{mess[3]}\n", keyboard)


    if mess_adm[0] == 'reg':
        try:
            reg = cl.Region(mess_adm[1], mess_adm[2], mess_adm[3], mess_adm[4], mess_adm[5], mess_adm[6])
            await reg.add_region()
            reg1 = defs.replace_name(mess_adm[1])
            await user.send_message(user.vk_id,f"Регион {reg1} добавлен.")
        except:
            await user.send_message(user.vk_id,"Введите команду по форме")
    if mess_adm[0] == 'road':
        reg = cl.Region(mess_adm[1], 0, 0, 0, 0, 0)
        await reg.load()
        await reg.add_road(mess_adm[2], mess_adm[3])
        reg1 = defs.replace_name(mess_adm[2])
        reg2 = defs.replace_name(reg.name)
        await user.send_message(user.vk_id,f"Путь между {reg1} и {reg2} был создан.")
    if mess_adm[0] == 'town':
        try:
            town = cl.Town(mess_adm[1], mess_adm[2], mess_adm[3])
            await town.add_town()
            await user.send_message(user.vk_id,f"Город {town.name} добавлен.")
        except:
            await user.send_message(user.vk_id,"Введите команду по форме")

# Отлавливаем новые посты
@setting.bot.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def wall_new_post(event: GroupTypes.WallPostNew):
    user = cl.User(setting.adm_id)
    await user.load()
    await user.send_message(setting.log_id, f"Создан пост №{event.object.id} от имени группы.")

    post = cl.Post(event.object.id)
    await post.add_post(0, event.object.text)
# Отлавливаем комментарии к постам
@setting.bot.on.raw_event(GroupEventType.WALL_REPLY_NEW, dataclass=GroupTypes.WallReplyNew)
async def wall_reply_new(event: GroupTypes.WallReplyNew):
    post = cl.Post(event.object.post_id)
    await post.load()

    if post.data + 24*60*60 > time.time():
            z = True
            for reply_id in json.loads(post.reply_ids):
                if int(event.object.from_id) == int(reply_id):
                    z = False

            if z:
                user = cl.User(event.object.from_id)
                await user.load()
                await post.add_reply(user.vk_id)
                await user.Cash(2000)
                await user.send_message(user.vk_id, f"{user.name}, вы оставили комментарий. Вы получили награду!")
                await user.send_message(setting.log_id, f"{user.name} оставил новый комментарий на пост №{post.id}.")
# Отлавливаем лайки
@setting.bot.on.raw_event(GroupEventType.LIKE_ADD, dataclass=GroupTypes.LikeAdd)
async def like_add(event: GroupTypes.LikeAdd):
    post = cl.Post(event.object.object_id)
    await post.load()

    if post.data + 24*60*60 > time.time():
            z = True
            for liker_id in json.loads(post.likers_ids):
                if int(event.object.liker_id) == int(liker_id):
                    z = False

            if z:
                user = cl.User(event.object.liker_id)
                await user.load()
                await post.add_like(user.vk_id)
                await user.Cash(2000)
                await user.send_message(user.vk_id, f"{user.name}, вы поставили лайк. Вы получили награду!")
                await user.send_message(setting.log_id, f"{user.name} поставил новый лайк на пост №{post.id}.")
# Отлавливаем удаление лайков
@setting.bot.on.raw_event(GroupEventType.LIKE_REMOVE, dataclass=GroupTypes.LikeRemove)
async def like_remove(event: GroupTypes.LikeRemove):

    if event.object.post_id == 0:
        number_post = event.object.object_id
    else: number_post = event.object.post_id

    post = cl.Post(number_post)
    await post.load()
    if post.avtor == 0:
        user = cl.User(event.object.liker_id)
        await user.load()
        await user.Cash(-2000)
        await user.send_message(user.vk_id, f"{user.name}, вы убрали лайк. Вы лишаетесь награды!")
        await user.send_message(setting.log_id, f"{user.name} убрал лайк на пост №{number_post}.")
# Отлавливаем удаление комментария
@setting.bot.on.raw_event(GroupEventType.WALL_REPLY_DELETE, dataclass=GroupTypes.WallReplyDelete)
async def wall_reply_delete(event: GroupTypes.WallReplyDelete):

    number_post = event.object.post_id
    post = cl.Post(number_post)
    await post.load()
    if post.avtor == 0:
        user = cl.User(event.object.deleter_id)
        await user.Cash(-2000)
        await user.send_message(user.vk_id, f"{user.name}, вы удалили комментарий. Вы получили штраф!")
        await user.send_message(setting.log_id, f"{user.name} удалил свой комментарий к посту №{number_post}.")

setting.bot.run_forever()