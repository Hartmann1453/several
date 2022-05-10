import random, defs
import json, aiosqlite, time
import setting, classes as cl
from vkbottle.bot import Message
from vkbottle.modules import json
from vkbottle import Keyboard, KeyboardButtonColor, Text

async def send_message(id, text):
    await setting.bot.api.messages.send(peer_ids=id, message=text, random_id=0)

async def timer(t):
    time.sleep(t)

async def load_all_users():
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT * FROM Users")
    result = await command.fetchall()
    await command.close()
    await connection.close()
    return result

async def biz_income():
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT * FROM Bisisnes")
    bizs = await command.fetchall()
    await command.close()
    await connection.close()

    for biz in bizs:
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {biz[5]}")
        owner = await command.fetchall()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{biz[4]}'")
        town = await command.fetchall()
        await command.close()
        await connection.close()

        inv = json.loads(owner[0][9])
        inv[f'{biz[4]}'][f'{biz[2]}'] += biz[3]
        inv[f'{biz[4]}']['зарплата'] += biz[7]
        inv[f'{biz[4]}']['налог'] += round(town[0][6] / 360)
        inv = json.dumps(inv, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET biz_income = '{inv}' WHERE bot_id = {biz[5]}")
        await connection.commit()
        await command.close()
        await connection.close()

async def peer_date(_average):

    _day = 16 * 60  # Длина дня в минутах
    _month = (_day * 30)  # Длина месяца в днях
    _year = (_day * 360)  # Длина года в днях

    now_time = round(time.time(), 0) - (_year * 2766)

    year = round(now_time // _year, 0)  # Текущий год
    month = round((now_time - (_year * year)) // _month, 0)  # Текущий месяц
    day = round((now_time - (_year * year) - (_month * month)) // _day, 0)  # Текущий день

    average = day
    if average != _average:
        _average = average
        await send_message(setting.log_id, f'Год: {year}\nМесяц: {month}\nДень: {day + 1}')
        print(f'Год: {year}\nМесяц: {month}\nДень: {day + 1}')
    return _average

async def peer_region_res():
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT * FROM Regions")
    regions = await command.fetchall()
    await command.close()
    await connection.close()

    for region in regions:
        region = cl.Region(region[0])
        await region.load()
        await region.regeneration_res()

async def peer_town():
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT * FROM Towns")
    towns = await command.fetchall()
    await command.close()
    await connection.close()

    for town in towns:
        town = cl.Town(town[0])
        await town.load()
        await town.consumption_res()

async def peer_hire():
    users = await load_all_users()

    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT * FROM Towns")
    towns = await command.fetchall()
    await command.close()
    await connection.close()

    for user in users:

        _user = cl.User(user[2])
        await _user.load()
        await _user.set_name()
        hire = json.loads(user[10])
        for town in towns:
            hire[town[0]]['наемный стрелок'] = random.randint(0, 5)
            hire[town[0]]['наемный воин'] = random.randint(0, 5)
            hire[town[0]]['наемный всадник'] = random.randint(0, 3)

        hire = json.dumps(hire, ensure_ascii=False)
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET hire = '{hire}' WHERE vk_id = {user[2]}")
        await connection.commit()
        await command.close()
        await connection.close()

async def check_tasks():
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT * FROM Tasks")
    tasks = await command.fetchall()
    await command.close()
    await connection.close()
    for task in tasks:
        if task[3] == 0:

            if task[1] == 'Перемещение':
                js_task = json.loads(task[2])

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Users SET location = '{js_task['target loc']}' WHERE vk_id = {js_task['vk_id']}")
                await connection.commit()
                await command.close()
                await connection.close()

                js_task['target loc'] = defs.replace_name(js_task['target loc'])

                keyboard = Keyboard()
                keyboard.add(Text("Осмотреться", {"payload": "чек ресурсов"}), color=KeyboardButtonColor.PRIMARY)
                keyboard.add(Text("Дороги", {"payload": "чек путей"}), color=KeyboardButtonColor.PRIMARY)
                keyboard.add(Text("Собирать", {"payload": "собирательство"}), color=KeyboardButtonColor.PRIMARY)
                keyboard.row()
                keyboard.add(Text("Искать поселение", {"payload": "войти в город"}), color=KeyboardButtonColor.SECONDARY)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                await connection.commit()
                await command.close()
                await connection.close()

                await cl.User.send_keyboard(cl.User, js_task['vk_id'], f"Вы добрались до {js_task['target loc']}", keyboard)
            if task[1] == 'Марш':
                js_task = json.loads(task[2])

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Flags SET location = '{js_task['target loc']}', status = 'Привал' WHERE flag_id = {js_task['flag_id']}")
                await connection.commit()
                await command.close()
                await connection.close()

                js_task['target loc'] = defs.replace_name(js_task['target loc'])

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = {js_task['flag_id']}")
                flag = await command.fetchone()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = {js_task['flag_id']}")
                commanders = await command.fetchall()
                await command.close()
                await connection.close()

                if flag[7] == 'Закрыт':
                    keyboard = Keyboard()
                    keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}),color=KeyboardButtonColor.PRIMARY)
                    keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.row()
                    keyboard.add(Text("Открыть набор", {"payload": f"Знамена|Открыть набор"}),color=KeyboardButtonColor.PRIMARY)
                    keyboard.row()
                    keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}),color=KeyboardButtonColor.SECONDARY)

                if flag[7] == 'Открыт':
                    keyboard = Keyboard()
                    keyboard.add(Text("Разведка", {"payload": f"Знамена|Разведка"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.add(Text("Информация", {"payload": f"Знамена|Информация"}),color=KeyboardButtonColor.PRIMARY)
                    keyboard.add(Text("Пути", {"payload": f"Знамена|Пути"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.row()
                    keyboard.add(Text("Закрыть набор", {"payload": f"Знамена|Закрыть набор"}),color=KeyboardButtonColor.PRIMARY)
                    keyboard.row()
                    keyboard.add(Text("Покинуть знамёна", {"payload": f"Знамена|Выйти"}),color=KeyboardButtonColor.SECONDARY)

                for commander in commanders:
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {commander[2]}")
                    us_commander = await command.fetchone()
                    await command.close()
                    await connection.close()

                    await cl.User.send_keyboard(cl.User, us_commander[2], f"Ваши знамёна добрались до {js_task['target loc']}.",keyboard)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                await connection.commit()
                await command.close()
                await connection.close()
            if task[1] == 'фарм рес':
                js_task = json.loads(task[2])

                user = cl.User(js_task['vk_id'])
                await user.load()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{js_task['город']}'")
                town = await command.fetchone()
                await command.close()
                await connection.close()

                inventar = json.loads(user.inventar)
                obrok = json.loads(town[11])

                obrok[f"{js_task['ресурс']}"] += js_task['оброк']
                inventar[f"{js_task['ресурс']}"] += js_task['количество'] - js_task['оброк']

                inventar = json.dumps(inventar, ensure_ascii=False)
                obrok = json.dumps(obrok, ensure_ascii=False)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Towns SET obrok = '{obrok}' WHERE name = '{js_task['город']}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Users SET inventar = '{inventar}', status = 'Нет' WHERE vk_id = '{js_task['vk_id']}'")
                await connection.commit()
                await command.close()
                await connection.close()

                keyboard = Keyboard()
                keyboard.add(Text("Осмотреться", {"payload": "чек ресурсов"}), color=KeyboardButtonColor.PRIMARY)
                keyboard.add(Text("Дороги", {"payload": "чек путей"}), color=KeyboardButtonColor.PRIMARY)
                keyboard.add(Text("Собирать", {"payload": "собирательство"}), color=KeyboardButtonColor.PRIMARY)
                keyboard.row()
                keyboard.add(Text("Искать поселение", {"payload": "войти в город"}), color=KeyboardButtonColor.SECONDARY)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                await connection.commit()
                await command.close()
                await connection.close()

                try:
                    if js_task['ресурс'] == 'рыба':
                        await cl.User.send_keyboard(cl.User, js_task['vk_id'], f"Вы окончили работу и поймали {js_task['количество']} рыбы. \nИз них {js_task['оброк']} ушло в казну в качестве оброка.", keyboard)
                    if js_task['ресурс'] == 'камень':
                        await cl.User.send_keyboard(cl.User, js_task['vk_id'], f"Вы окончили работу и добыли {js_task['количество']} камня. \nИз них {js_task['оброк']} ушло в казну в качестве оброка.", keyboard)
                    if js_task['ресурс'] == 'руда':
                        await cl.User.send_keyboard(cl.User, js_task['vk_id'], f"Вы окончили работу и добыли {js_task['количество']} руды. \nИз них {js_task['оброк']} ушло в казну в качестве оброка.", keyboard)
                    if js_task['ресурс'] == 'дерево':
                        await cl.User.send_keyboard(cl.User, js_task['vk_id'], f"Вы окончили работу и добыли {js_task['количество']} дерева. \nИз них {js_task['оброк']} ушло в казну в качестве оброка.", keyboard)
                    if js_task['ресурс'] == 'хлопок':
                        await cl.User.send_keyboard(cl.User, js_task['vk_id'], f"Вы окончили работу и собрали {js_task['количество']} хлопка. \nИз них {js_task['оброк']} ушло в казну в качестве оброка.", keyboard)
                except:
                    await cl.User.send_message(cl.User, setting.log_id, f"Ошибка отправления сообщения игроку {js_task['vk_id']}")
            if task[1] == 'Постройка бизнеса':

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT MAX(id) FROM Bisisnes")
                result = await command.fetchone()
                await command.close()
                await connection.close()

                js_task = json.loads(task[2])

                id = result[0] + 1
                res = js_task['ресурс']
                type_biz = js_task['тип бизнеса']
                income = js_task['доход']
                town = js_task['город']
                owner_id = js_task['bot_id']
                owner_name = js_task['name']
                payment = js_task['зарплата']
                await cl.Town.add_biz(cl.Town, id, type_biz, res, income, town, owner_id, owner_name, payment)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                await connection.commit()
                await command.close()
                await connection.close()

                await cl.User.send_message(cl.User, js_task['vk_id'], f"Ваш бизнес достроен в городе {town}.[{type_biz}]")
            if task[1] == 'Обучение солдат':
                js_task = json.loads(task[2])

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{js_task['город']}'")
                town = await command.fetchone()
                await command.close()
                await connection.close()

                garnizon = json.loads(town[9])
                garnizon[f"{js_task['тип солдат']}"] += js_task['количество солдат']

                garnizon = json.dumps(garnizon, ensure_ascii=False)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(
                    f"UPDATE Towns SET garnizon = '{garnizon}' WHERE name = '{js_task['город']}'")
                await connection.commit()
                await command.close()
                await connection.close()

                await cl.User.send_message(cl.User, js_task['vk_id'], f"Обучение солдат в городе {js_task['город']} закончено. [{js_task['тип солдат']}:{js_task['количество солдат']}]")

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                await connection.commit()
                await command.close()
                await connection.close()

            if task[1] == 'Сражение за город':
                js_task = json.loads(task[2])

                # Запрашиваем флаг командира
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = {js_task['Номер знамени']}")
                flag = await command.fetchone()
                await command.close()
                await connection.close()

                # Узнаем локацию нашего флага
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{flag[4]}'")
                region = await command.fetchone()
                await command.close()
                await connection.close()

                # Запрашиваем город в локации
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{region[2]}'")
                town = await command.fetchone()
                await command.close()
                await connection.close()

                # Запрашиваем всех игроков во флаге нападения
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Flags WHERE flag_id = {flag[3]}")
                army = await command.fetchall()
                await command.close()
                await connection.close()

                # Находим владельца города
                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {town[3]}")
                king = await command.fetchone()
                await command.close()
                await connection.close()

                # Считаем общие войска флага
                army_union = {
                    "рекруты": 0,
                    "ополченец": 0,
                    "стрелок": 0,
                    "всадник": 0,
                    "воин": 0,
                    "наемный стрелок": 0,
                    "наемный всадник": 0,
                    "наемный воин": 0
                }

                for unity_flag in army:
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {unity_flag[2]}")
                    unit_user = await command.fetchone()
                    await command.close()
                    await connection.close()

                    json_res = json.loads(unit_user[5])

                    for key, value in json_res.items():
                        army_union[key] += value

                # Запрашиваем гарнизон города
                garnizon = json.loads(town[9])

                # Проводим бой с помощью функции
                army_union_after, garnizon_after = await defs.fight(army_union.copy(), garnizon.copy())

                # Убираем отрицательные значения войск
                for soldair_type_key, soldair_type_value in army_union_after.items():
                    if soldair_type_value < 0:
                        army_union_after[soldair_type_key] = 0

                for soldair_type_key, soldair_type_value in garnizon_after.items():
                    if soldair_type_value < 0:
                        garnizon_after[soldair_type_key] = 0


                # Считаем потери сторон
                miss = {}
                miss['атака'] = {}
                miss['защита'] = {}

                for soldair_type_key, soldair_type_value in army_union.items():
                    miss['атака'][soldair_type_key] = soldair_type_value - army_union_after[soldair_type_key]

                for soldair_type_key, soldair_type_value in garnizon.items():
                    miss['защита'][soldair_type_key] = soldair_type_value - garnizon_after[soldair_type_key]

                # Считаем доли игроков флага в армии
                # Сохраняем новое значение армии игрока
                # Оповещаем игрока о потерях в посследнем бою.
                for unity_flag in army:
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {unity_flag[2]}")
                    unit_user = await command.fetchone()
                    await command.close()
                    await connection.close()
                    player_miss = {}
                    json_res = json.loads(unit_user[5])
                    txt = 'Отчет о потерях в последнем бою:\n'
                    for key, value in json_res.items():
                        if army_union[key] / 100 == 0:
                            player_median = 0
                        else:
                            player_median = round(value / (army_union[key] / 100), 2)

                        player_miss[key] = int(round((miss['атака'][key] / 100) * player_median))
                        json_res[key] = int(value - player_miss[key])
                        txt += f"{key}: {player_miss[key]}\n"

                    json_res = json.dumps(json_res, ensure_ascii=False)

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Users SET army = '{json_res}' WHERE bot_id = {unity_flag[2]}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    await cl.User.send_message(cl.User, unit_user[2], txt)

                # Отравляем отчет о бое владельцу города
                # Сохраняем изменения войск города
                txt = f'Отчёт о потерях в бою за {region[2]}:\n'
                for key, value in miss['защита'].items():
                    txt += f'{key}: {value}\n'

                garnizon_after = json.dumps(garnizon_after, ensure_ascii=False)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Towns SET garnizon = '{garnizon_after}' WHERE name = '{region[2]}'")
                await connection.commit()
                await command.close()
                await connection.close()

                await cl.User.send_message(cl.User, king[2], txt)

                # Проверяем окончание сражения.
                garnizon_after = json.loads(garnizon_after)
                count = 0
                for key, value in garnizon_after.items():
                    if key != 'рекруты':
                        count += value
                # Проверяем количество солдат в гарнизоне

                if count == 0:
                    # Сценарий поражения города

                    # Обновляем владельца города
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Towns SET king = {flag[5]} WHERE name = '{region[2]}'")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    # Сообщение для бывшего владельца города

                    keyboard = Keyboard()
                    keyboard.add(Text("Окраина", {"payload": "Окраина"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.add(Text("Информация", {"payload": "Инфо город"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.add(Text("Рынок", {"payload": "Рынок"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.row()
                    keyboard.add(Text("Таверна", {"payload": "Таверна"}), color=KeyboardButtonColor.PRIMARY)
                    keyboard.row()
                    keyboard.add(Text("Покинуть город", {"payload": "Покинуть город"}),color=KeyboardButtonColor.SECONDARY)

                    await cl.User.send_keyboard(cl.User, king[2], f'Гарнизон города {region[2]} пал.\nВы утратили контроль над городом.', keyboard)

                    # Сообщение для нового владельца города
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {flag[5]}")
                    commander_flag = await command.fetchone()
                    await command.close()
                    await connection.close()

                    await cl.User.send_message(cl.User, commander_flag[2],f'Гарнизон города {region[2]} пал.\nВы получили контроль над городом.\nНужно как можно быстрее разместить в нём гарнизон!')

                    # Удаляем задачу т.к. сражение окончено
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Flags SET status = 'Привал' WHERE flag_id = {flag[3]}")
                    await connection.commit()
                    await command.close()
                    await connection.close()


                # Проверяем количесство солдат в атакующем флаге
                count = 0
                for key, value in army_union_after.items():
                    if key != 'рекруты':
                        count += value

                if count == 0:
                    # Сценарий поражения знамени


                    # Сообщения для владельца города.
                    await cl.User.send_message(cl.User, king[2], f'Гарнизон города {region[2]} выдержал натиск!\n Контроль над городом сохранен!')

                    # Сообщения для владельца знамени.
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {flag[5]}")
                    commander_flag = await command.fetchone()
                    await command.close()
                    await connection.close()

                    await cl.User.send_message(cl.User, commander_flag[2],f'Вы потерпели окончательное поражение в битве за город {region[2]}.\nБой окончен.')

                    # Удаляем задачу т.к. сражение окончено
                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"DELETE FROM Tasks WHERE id = {task[0]}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

                    connection = await aiosqlite.connect(setting.db)
                    command = await connection.execute(f"UPDATE Flags SET status = 'Привал' WHERE flag_id = {flag[3]}")
                    await connection.commit()
                    await command.close()
                    await connection.close()

        else:
            nw_data = task[3] - 1
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(
                f"UPDATE Tasks SET data = {nw_data} WHERE id = {task[0]}")
            await connection.commit()
            await command.close()
            await connection.close()

@setting.bot.on.message()
async def message_handler(message: Message):
    mess = message.text.lower()
    _average = 0
    if mess == 'пиринг' and (message.from_id == 553709956 or message.from_id == 257368093):
        await send_message(message.from_id, f"пир")
        while True:
            _average = await peer_date(_average)
            await peer_region_res()
            await peer_town()
            await biz_income()
            await peer_hire()
            await check_tasks()
            #await timer(16 * 60) # 1 рп-день
            await timer(5) # 1 рп-день

setting.bot.run_forever()