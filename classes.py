import random
import time
import defs, setting
import json, aiosqlite
from vkbottle.modules import json
from vkbottle import Keyboard, KeyboardButtonColor, Text


class User:

    def __init__(self, vk_id):
        self.bot_id = 1
        self.vk_id = vk_id
        self.cash = 0
        self.rep = 0
        self.army = 0
        self.army = json.dumps({
            'рекруты': 0,
            'ополченец': 0,
            'стрелок': 0,
            'всадник': 0,
            'воин': 0,
            'наемный стрелок': 0,
            'наемный всадник': 0,
            'наемный воин': 0
        }, ensure_ascii=False)
        self.name = 'Новорег'
        self.location = 'Хартмарк'
        self.status = 'Нет'
        self.inventar = json.dumps({
            'рыба': 0,
            'камень': 0,
            'руда': 0,
            'дерево': 0,
            'хлопок': 0
        }, ensure_ascii=False)
        self.biz_income = json.dumps({
            self.location: {
            'рыба': 0,
            'камень': 0,
            'руда': 0,
            'дерево': 0,
            'хлопок': 0,
            'налог': 0,
            'зарплата': 0
            }
        }, ensure_ascii=False)
        self.hire = json.dumps({
            self.location: {
            'наемный стрелок': 0,
            'наемный воин': 0,
            'наемный всадник': 0
            }
        }, ensure_ascii=False)

    async def add_user(self, bot_id):
        connection = await aiosqlite.connect(setting.db)
        if self.vk_id > 0:
            command = await connection.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            bot_id, self.name, self.vk_id, self.cash, self.rep, self.army, self.location, self.status, self.inventar, self.biz_income, self.hire))
            await connection.commit()
            await command.close()
            keyboard = Keyboard()

            keyboard.add(Text("Начать", {"payload":"Начать"}), color=KeyboardButtonColor.POSITIVE)
            #keyboard.add(Text("Красный", {"payload":"Красный"}), color=KeyboardButtonColor.NEGATIVE)
            #keyboard.add(Text("Синий", {"payload":"Синий"}), color=KeyboardButtonColor.PRIMARY)

            #keyboard.row()

            #keyboard.add(Text("Зеленый", {"payload":"Зеленый"}), color=KeyboardButtonColor.POSITIVE)
            #keyboard.add(Text("Белый", {"payload":"Белый"}), color=KeyboardButtonColor.SECONDARY)

            await self.send_keyboard(self.vk_id,"Вы успешно зарегистрированы.", keyboard)
        await connection.close()
    async def load(self):
        try:
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Users WHERE vk_id = {self.vk_id}")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            self.bot_id = result[0]
            await User.get_user_name(self)
            self.vk_id = result[2]
            self.cash = result[3]
            self.rep = result[4]
            self.army = result[5]
            self.location = result[6]
            self.status = result[7]
            self.inventar = result[8]
            self.biz_income = result[9]
            self.hire = result[10]


        except:
            bot_id = await User.last_insert(self)
            bot_id += 1
            await User.add_user(self, bot_id)
    async def load_bot_id(self, bot_id):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = {bot_id}")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        self.bot_id = result[0]
        self.vk_id = result[2]
        await User.get_user_name(self)
        self.cash = result[3]
        self.rep = result[4]
        self.army = result[5]
        self.location = result[6]
        self.status = result[7]
    async def set_name(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET name = '{self.name}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()
    async def get_user_name(self):
        user = await setting.bot.api.users.get(self.vk_id)
        self.name = str(user[0].first_name) + ' ' + str(user[0].last_name)
    async def last_insert(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT MAX(bot_id) FROM Users")
        result = await command.fetchone()
        await command.close()
        await connection.close()
        result = result[0]
        return result

    async def send_message(self, vk_id, text):
        await setting.bot.api.messages.send(peer_ids=vk_id, message=text, random_id=0)
    async def send_keyboard(self, vk_id, text, keyboard):
        await setting.bot.api.messages.send(peer_ids=vk_id, message=text, random_id=0, keyboard=keyboard)

    async def exit(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        town = defs.replace_name(self.location)
        self.location = result[2]
        reg = defs.replace_name(result[2])

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET location = '{self.location}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Осмотреться", {"payload": "чек ресурсов"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Дороги", {"payload": "чек путей"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Собирать", {"payload": "собирательство"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Искать поселение", {"payload": "войти в город"}), color=KeyboardButtonColor.SECONDARY)

        await self.send_keyboard(self.vk_id, f"Вы вышли из города {town} и перешли в {reg}.", keyboard)
    async def inside(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()


        if (result[2] == 'Нет'):
            await self.send_message(self.vk_id, f"В этой локации нет города.")
        else:
            self.location = result[2]

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(
                f"UPDATE Users SET location = '{self.location}' WHERE vk_id = {self.vk_id}")
            await connection.commit()
            await command.close()
            await connection.close()

            keyboard = Keyboard()
            keyboard.add(Text("Окраина", {"payload": "Окраина"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Информация", {"payload": "Инфо город"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.add(Text("Рынок", {"payload": "Рынок"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Таверна", {"payload": "Таверна"}), color=KeyboardButtonColor.PRIMARY)
            if self.bot_id == town[3]:
                keyboard.row()
                keyboard.add(Text("Дворец", {"payload": "Дворец"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Покинуть город", {"payload": "Покинуть город"}), color=KeyboardButtonColor.SECONDARY)

            await self.send_keyboard(self.vk_id, f"Вы вошли на центральную площадь города {self.location}.", keyboard)
    async def travel(self, number):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()
        roads = json.loads(result[1])
        i = 0
        for road in roads.keys():
            i += 1

            if i == number:

                json_res = {
                    'vk_id': self.vk_id,
                    'target loc': road
                }
                json_res = json.dumps(json_res, ensure_ascii=False)
                data_time = round(int(roads[f'{road}']) / 10)
                await defs.create_task('Перемещение', json_res, data_time)

    async def Cash(self, count):
        self.cash += count
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash + {count} WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

    async def see_loc(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()
        try:
            roads = json.loads(result[1])
            i = 0
            keyboard = Keyboard()
            for road in roads.keys():
                i += 1
                road_rep = defs.replace_name(road)
                keyboard.add(Text(road_rep, {"payload": f"Путь{i}"}), color=KeyboardButtonColor.PRIMARY)
            keyboard.row()
            keyboard.add(Text("Назад", {"payload": f"В провинцию"}), color=KeyboardButtonColor.SECONDARY)
            await self.send_keyboard(self.vk_id, f"Куда направляемся?", keyboard)
        except:
            await self.send_message(self.vk_id, f"В городе нельзя осматриваться.")
    async def check_res(self):
        try:
            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            reg = defs.replace_name(self.location)
            await self.send_message(self.vk_id,
                                f"Ресурсы провинции {reg}:\nРыба:{result[7]}\nКамень:{result[3]}\nРуда:{result[5]}\nДерево:{result[4]}\nХлопок:{result[6]}\n")
        except: await self.send_message(self.vk_id,f"Нужно покинуть город")
    async def mine_stone(self):

            if self.status == 'Работа':
                await self.send_message(self.vk_id, "Вы уже работаете.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{result[8]}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            resource = result[3]
            farm_count = random.randint(25, 50)

            if resource > 0:

                resource -= farm_count

                if resource < 0:
                    farm_count += resource
                    resource = 0

                tax_reg = round(farm_count * (town[7] / 100))
                js_task = {
                    "vk_id": self.vk_id,
                    "ресурс": "камень",
                    "количество": farm_count,
                    "оброк": tax_reg,
                    "город": town[0]
                }
                js_task = json.dumps(js_task, ensure_ascii=False)
                await defs.create_task('фарм рес', js_task, 0)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Regions SET stone = {resource} WHERE name = '{self.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Users SET status = 'Работа' WHERE vk_id = {self.vk_id}")
                await connection.commit()
                await command.close()
                await connection.close()
                keyboard = Keyboard()
                keyboard.add(Text("Работа", {"payload": "Работа|Чек"}), color=KeyboardButtonColor.PRIMARY)

                await self.send_keyboard(self.vk_id, f"Вы начали добычу камня, это займет целый день.", keyboard)
            else: await self.send_message(self.vk_id, "В провинции кончился камень")
    async def mine_tree(self):

            if self.status == 'Работа':
                await self.send_message(self.vk_id, "Вы уже работаете.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{result[8]}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            resource = result[4]
            farm_count = random.randint(25, 50)

            if resource > 0:

                resource -= farm_count

                if resource < 0:
                    farm_count += resource
                    resource = 0

                tax_reg = round(farm_count * (town[7] / 100))
                js_task = {
                    "vk_id": self.vk_id,
                    "ресурс": "дерево",
                    "количество": farm_count,
                    "оброк": tax_reg,
                    "город": town[0]
                }
                js_task = json.dumps(js_task, ensure_ascii=False)
                await defs.create_task('фарм рес', js_task, 0)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Regions SET tree = {resource} WHERE name = '{self.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Users SET status = 'Работа' WHERE vk_id = {self.vk_id}")
                await connection.commit()
                await command.close()
                await connection.close()

                keyboard = Keyboard()
                keyboard.add(Text("Работа", {"payload": "Работа|Чек"}), color=KeyboardButtonColor.PRIMARY)

                await self.send_keyboard(self.vk_id, f"Вы начали добычу дерева, это займет целый день.", keyboard)
            else: await self.send_message(self.vk_id, "В провинции кончилось дерево")
    async def mine_ore(self):

            if self.status == 'Работа':
                await self.send_message(self.vk_id, "Вы уже работаете.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{result[8]}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            resource = result[5]
            farm_count = random.randint(5, 15)

            if resource > 0:

                resource -= farm_count

                if resource < 0:
                    farm_count += resource
                    resource = 0

                tax_reg = round(farm_count * (town[7] / 100))
                js_task = {
                    "vk_id": self.vk_id,
                    "ресурс": "руда",
                    "количество": farm_count,
                    "оброк": tax_reg,
                    "город": town[0]
                }
                js_task = json.dumps(js_task, ensure_ascii=False)
                await defs.create_task('фарм рес', js_task, 0)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Regions SET ore = {resource} WHERE name = '{self.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Users SET status = 'Работа' WHERE vk_id = {self.vk_id}")
                await connection.commit()
                await command.close()
                await connection.close()

                keyboard = Keyboard()
                keyboard.add(Text("Работа", {"payload": "Работа|Чек"}), color=KeyboardButtonColor.PRIMARY)

                await self.send_keyboard(self.vk_id, f"Вы начали добычу руды, это займет целый день.", keyboard)

            else: await self.send_message(self.vk_id, "В провинции кончилась руда")
    async def mine_silk(self):

            if self.status == 'Работа':
                await self.send_message(self.vk_id, "Вы уже работаете.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{result[8]}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            resource = result[6]
            farm_count = random.randint(30, 60)

            if resource > 0:

                resource -= farm_count

                if resource < 0:
                    farm_count += resource
                    resource = 0

                tax_reg = round(farm_count * (town[7] / 100))
                js_task = {
                    "vk_id": self.vk_id,
                    "ресурс": "хлопок",
                    "количество": farm_count,
                    "оброк": tax_reg,
                    "город": town[0]
                }
                js_task = json.dumps(js_task, ensure_ascii=False)
                await defs.create_task('фарм рес', js_task, 0)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Regions SET silk = {resource} WHERE name = '{self.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Users SET status = 'Работа' WHERE vk_id = {self.vk_id}")
                await connection.commit()
                await command.close()
                await connection.close()

                keyboard = Keyboard()
                keyboard.add(Text("Работа", {"payload": "Работа|Чек"}), color=KeyboardButtonColor.PRIMARY)

                await self.send_keyboard(self.vk_id, f"Вы начали сбор хлопка, это займет целый день.", keyboard)
            else: await self.send_message(self.vk_id, "В провинции кончился хлопок")
    async def fishing(self):

            if self.status == 'Работа':
                await self.send_message(self.vk_id, "Вы уже работаете.")
                return

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
            result = await command.fetchone()
            await command.close()
            await connection.close()

            connection = await aiosqlite.connect(setting.db)
            command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{result[8]}'")
            town = await command.fetchone()
            await command.close()
            await connection.close()

            resource = result[7]
            farm_count = random.randint(100, 200)

            if resource > 0:

                resource -= farm_count

                if resource < 0:
                    farm_count += resource
                    resource = 0

                tax_reg = round(farm_count * (town[7] / 100))
                js_task = {
                    "vk_id": self.vk_id,
                    "ресурс": "рыба",
                    "количество": farm_count,
                    "оброк": tax_reg,
                    "город": town[0]
                }
                js_task = json.dumps(js_task, ensure_ascii=False)
                await defs.create_task('фарм рес', js_task, 0)

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Regions SET fish = {resource} WHERE name = '{self.location}'")
                await connection.commit()
                await command.close()
                await connection.close()

                connection = await aiosqlite.connect(setting.db)
                command = await connection.execute(f"UPDATE Users SET status = 'Работа' WHERE vk_id = {self.vk_id}")
                await connection.commit()
                await command.close()
                await connection.close()

                keyboard = Keyboard()
                keyboard.add(Text("Работа", {"payload": "Работа|Чек"}), color=KeyboardButtonColor.PRIMARY)

                await self.send_keyboard(self.vk_id, f"Вы начали рыбалку, это займет целый день.", keyboard)
            else: await self.send_message(self.vk_id, "В провинции кончилась рыба")

    async def sell_stone(self):
        count = 100

        inventar = json.loads(self.inventar)
        if inventar['камень'] < count:
            count = inventar['камень']

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(result[4])
        market['Склад']['камень'] += count
        income = market['Цена']['камень'] * count
        market = json.dumps(market, ensure_ascii=False)

        inventar['камень'] -= count
        inventar = json.dumps(inventar, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash + {income}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы продали {count} камня за {income} монет.")
    async def sell_tree(self):
        count = 100

        inventar = json.loads(self.inventar)
        if inventar['дерево'] < count:
            count = inventar['дерево']

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(result[4])
        market['Склад']['дерево'] += count
        income = market['Цена']['дерево'] * count
        market = json.dumps(market, ensure_ascii=False)

        inventar['дерево'] -= count
        inventar = json.dumps(inventar, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash + {income}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы продали {count} дерева за {income} монет.")
    async def sell_ore(self):
        count = 100

        inventar = json.loads(self.inventar)
        if inventar['руда'] < count:
            count = inventar['руда']

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(result[4])
        market['Склад']['руда'] += count
        income = market['Цена']['руда'] * count
        market = json.dumps(market, ensure_ascii=False)

        inventar['руда'] -= count
        inventar = json.dumps(inventar, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash + {income}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы продали {count} руды за {income} монет.")
    async def sell_silk(self):
        count = 100

        inventar = json.loads(self.inventar)
        if inventar['хлопок'] < count:
            count = inventar['хлопок']

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(result[4])
        market['Склад']['хлопок'] += count
        income = market['Цена']['хлопок'] * count
        market = json.dumps(market, ensure_ascii=False)

        inventar['хлопок'] -= count
        inventar = json.dumps(inventar, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash + {income}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы продали {count} хлопка за {income} монет.")
    async def sell_fish(self):
        count = 100

        inventar = json.loads(self.inventar)
        if inventar['рыба'] < count:
            count = inventar['рыба']

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(result[4])
        market['Склад']['рыба'] += count
        income = market['Цена']['рыба'] * count
        market = json.dumps(market, ensure_ascii=False)

        inventar['рыба'] -= count
        inventar = json.dumps(inventar, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash + {income}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы продали {count} рыбы за {income} монет.")
    async def buy_stone(self):
        count = 100


        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        inventar = json.loads(self.inventar)
        market = json.loads(result[4])
        market['Склад']['камень'] -= count
        price = market['Цена']['камень'] * count

        if self.cash < price:
            await self.send_message(self.vk_id, "У вас недостаточно денег.")
            return

        if market['Склад']['камень'] < 0:
            await self.send_message(self.vk_id, "На рынке не хватает камня.")
            return
        inventar['камень'] += count
        inventar = json.dumps(inventar, ensure_ascii=False)
        market = json.dumps(market, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash - {price}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы купили {count} камня за {price} монет.")
    async def buy_tree(self):
        count = 100


        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        inventar = json.loads(self.inventar)
        market = json.loads(result[4])
        market['Склад']['дерево'] -= count
        price = market['Цена']['дерево'] * count

        if self.cash < price:
            await self.send_message(self.vk_id, "У вас недостаточно денег.")
            return

        if market['Склад']['дерево'] < 0:
            await self.send_message(self.vk_id, "На рынке не хватает дерева.")
            return

        inventar['дерево'] += count
        inventar = json.dumps(inventar, ensure_ascii=False)
        market = json.dumps(market, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash - {price}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы купили {count} дерева за {price} монет.")
    async def buy_ore(self):
        count = 100


        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        inventar = json.loads(self.inventar)
        market = json.loads(result[4])
        market['Склад']['руда'] -= count
        price = market['Цена']['руда'] * count

        if self.cash < price:
            await self.send_message(self.vk_id, "У вас недостаточно денег.")
            return
        if market['Склад']['руда'] < 0:
            await self.send_message(self.vk_id, "На рынке не хватает руды.")
            return

        inventar['руда'] += count
        inventar = json.dumps(inventar, ensure_ascii=False)
        market = json.dumps(market, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash - {price}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы купили {count} руды за {price} монет.")
    async def buy_silk(self):
        count = 100


        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        inventar = json.loads(self.inventar)
        market = json.loads(result[4])
        market['Склад']['хлопок'] -= count
        price = market['Цена']['хлопок'] * count

        if self.cash < price:
            await self.send_message(self.vk_id, "У вас недостаточно денег.")
            return
        if market['Склад']['хлопок'] < 0:
            await self.send_message(self.vk_id, "На рынке не хватает хлопка.")
            return

        inventar['хлопок'] += count
        inventar = json.dumps(inventar, ensure_ascii=False)
        market = json.dumps(market, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash - {price}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы купили {count} хлопка за {price} монет.")
    async def buy_fish(self):
        count = 100


        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        inventar = json.loads(self.inventar)
        market = json.loads(result[4])
        market['Склад']['рыба'] -= count
        price = market['Цена']['рыба'] * count

        if self.cash < price:
            await self.send_message(self.vk_id, "У вас недостаточно денег.")
            return
        if market['Склад']['рыба'] < 0:
            await self.send_message(self.vk_id, "На рынке не хватает рыбы.")
            return

        inventar['рыба'] += count
        inventar = json.dumps(inventar, ensure_ascii=False)
        market = json.dumps(market, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET market = '{market}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = cash - {price}, inventar = '{inventar}' WHERE vk_id = {self.vk_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        await self.send_message(self.vk_id, f"Вы купили {count} рыбы за {price} монет.")

    async def check_biz(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Bisisnes WHERE owner_id = {self.bot_id}")
        bizs = await command.fetchall()
        await command.close()
        await connection.close()

        txt = f'Стоимость предприятий:\n' \
              f"Рыболовное судно: 1500 сер. {setting.price['Рыб.Судно']['дерево']} дер. {setting.price['Рыб.Судно']['хлопок']} хлопка\n" \
              f"Плантация Хлопка: 1500 сер. {setting.price['Плантация хлопка']['дерево']} дер. {setting.price['Плантация хлопка']['хлопок']} хлопка и 100 камня\n" \
              f"Лесопилка: 1500 сер. {setting.price['Лесопилка']['дерево']} дер. {setting.price['Лесопилка']['хлопок']} хлопка, {setting.price['Лесопилка']['руда']} руды и {setting.price['Лесопилка']['камень']} камня\n" \
              f"Каменоломня: 1500 сер. {setting.price['Каменоломня']['дерево']} дер. {setting.price['Каменоломня']['хлопок']} хлопка, {setting.price['Каменоломня']['руда']} руды и {setting.price['Каменоломня']['камень']} камня\n" \
              f"Шахта: 1500 сер. {setting.price['Шахта']['дерево']} дер. {setting.price['Шахта']['хлопок']} хлопка, {setting.price['Шахта']['руда']} руды и {setting.price['Шахта']['камень']} камня\n" \
              f'\n' \
              f'Материал для строительства берется с рынка по текущей цене.\n'

        _i = 0
        i = {
            'рыба': 0,
            'хлопок': 0,
            'дерево': 0,
            'камень': 0,
            'руда': 0
        }
        for biz in bizs:
            if biz[1] == 'Рыб.Судно':
                i['рыба'] += 1
                _i = 1
            if biz[1] == 'Плантация хлопка':
                i['хлопок'] += 1
                _i = 1
            if biz[1] == 'Лесопилка':
                i['дерево'] += 1
                _i = 1
            if biz[1] == 'Каменоломня':
                i['камень'] += 1
                _i = 1
            if biz[1] == 'Шахта':
                i['руда'] += 1
                _i = 1

        if _i == 1:
            txt += f'\n\nНа окраине города {self.location} у вас есть следующие предприятия:\n'

        if i['рыба'] > 0:
            txt += f"Рыб.судна: {i['рыба']}\n"
        if i['хлопок'] > 0:
            txt += f"Плантации хлопка: {i['хлопок']}\n"
        if i['дерево'] > 0:
            txt += f"Лесопилки: {i['дерево']}\n"
        if i['камень'] > 0:
            txt += f"Каменоломни: {i['камень']}\n"
        if i['руда'] > 0:
            txt += f"Шахты: {i['руда']}\n"

        await self.send_message(self.vk_id, txt)
    async def check_inventar(self):

        inventar = json.loads(self.inventar)
        await User.send_message(self, self.vk_id,
                                f"Ваш инвентарь:\nКамень: {inventar['камень']}\nРуда: {inventar['руда']}\nХлопок: {inventar['хлопок']}\nДерево: {inventar['дерево']}\nРыба: {inventar['рыба']}")
    async def check_army(self):

        army = json.loads(self.army)
        await User.send_message(self, self.vk_id,
                                f"Ваши знамёна:"
                                f"\nРекруты: {army['рекруты']}"
                                f"\nОполченцы: {army['ополченец']}"
                                f"\nСтрелки: {army['стрелок']}"
                                f"\nВсадники: {army['всадник']}"
                                f"\nВоины: {army['воин']}"
                                f"\nНаемные стрелки: {army['наемный стрелок']}"
                                f"\nНаемные всадники: {army['наемный всадник']}"
                                f"\nНаемные воины: {army['наемный воин']}")
    async def passport(self):
        loc = defs.replace_name(self.location)
        await User.send_message(self, self.vk_id,
                                f"Номер паспорта: {self.bot_id}\nИмя: {self.name}\nБаланс: {round(self.cash)}\nРепутация: {self.rep}\nЛокация: {loc}")
    async def town_info(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = '{result[3]}'")
        king = await command.fetchone()
        await command.close()
        await connection.close()
        print(result)
        await self.send_message(self.vk_id, f"Город: {result[0]}\nНаселение: {result[1]}\nПравитель: {king[1]}\nНалог на землю: {result[6]}\nОброк: {result[7]}%")
    async def market_info(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(result[4])

        keyboard = Keyboard()
        keyboard.add(Text("Продать ресурсы", {"payload": "продажа ресов"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Купить ресурсы", {"payload": "покупка ресов"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Инструменты", {"payload": "Инструменты"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Назад", {"payload": "город"}), color=KeyboardButtonColor.SECONDARY)

        if market['Склад']['камень'] < 0:
            market['Склад']['камень'] = 0

        if market['Склад']['дерево'] < 0:
            market['Склад']['дерево'] = 0

        if market['Склад']['руда'] < 0:
            market['Склад']['руда'] = 0

        if market['Склад']['хлопок'] < 0:
            market['Склад']['хлопок'] = 0

        if market['Склад']['рыба'] < 0:
            market['Склад']['рыба'] = 0


        await self.send_keyboard(self.vk_id, f"Рынок города {result[0]}:\n"
                                            f"Камень: {market['Склад']['камень']} шт. по {market['Цена']['камень']} серебра.\n"
                                            f"Руда: {market['Склад']['руда']} шт. по {market['Цена']['руда']} серебра.\n"
                                            f"Дерево: {market['Склад']['дерево']} шт. по {market['Цена']['дерево']} серебра.\n"
                                            f"Хлопок: {market['Склад']['хлопок']} шт. по {market['Цена']['хлопок']} серебра.\n"
                                            f"Рыба: {market['Склад']['рыба']} шт. по {market['Цена']['рыба']} серебра.", keyboard)
    async def start_work(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.location}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        if result[3] > 0:
            _i = 1
            keyboard.add(Text("Добывать камень", {"payload": "фарм камня"}), color=KeyboardButtonColor.PRIMARY)
        if result[4] > 0:
            _i = 1
            keyboard.add(Text("Рубить дерево", {"payload": "фарм дерева"}), color=KeyboardButtonColor.PRIMARY)
        if result[5] > 0:
            _i = 1
            keyboard.add(Text("Добывать руду", {"payload": "фарм руды"}), color=KeyboardButtonColor.PRIMARY)
        if result[6] > 0:
            _i = 1
            keyboard.add(Text("Собирать хлопок", {"payload": "фарм хлопка"}), color=KeyboardButtonColor.PRIMARY)
        if result[7] > 0:
            _i = 1
            keyboard.add(Text("Ловить рыбу", {"payload": "фарм рыбы"}), color=KeyboardButtonColor.PRIMARY)
        if _i == 1:
            keyboard.row()
        keyboard.add(Text("Назад", {"payload": "В провинцию"}), color=KeyboardButtonColor.SECONDARY)
        await self.send_keyboard(self.vk_id, "Какой ресурс вы хотите добывать?", keyboard)
    async def pretown(self):

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        keyboard = Keyboard()
        keyboard.add(Text("Информация", {"payload": "Инфо окраины"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        specialization = json.loads(town[10])
        for spec in specialization:
            if spec == 'рыба':
                keyboard.add(Text("Рыб.Судно", {"payload": "бизнес"}), color=KeyboardButtonColor.PRIMARY)
            if spec == 'хлопок':
                keyboard.add(Text("Плантация хлопка", {"payload": "бизнес"}), color=KeyboardButtonColor.PRIMARY)
            if spec == 'дерево':
                keyboard.add(Text("Лесопилка", {"payload": "бизнес"}), color=KeyboardButtonColor.PRIMARY)
            if spec == 'камень':
                keyboard.add(Text("Каменоломня", {"payload": "бизнес"}), color=KeyboardButtonColor.PRIMARY)
            if spec == 'руда':
                keyboard.add(Text("Шахта", {"payload": "бизнес"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Собрать ресурсы", {"payload": "Сбор"}), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()
        keyboard.add(Text("Вернуться на площадь", {"payload": "город"}), color=KeyboardButtonColor.SECONDARY)

        await self.send_keyboard(self.vk_id,f"Вы вышли на окраину города {self.location}.", keyboard)

    async def harvest(self):

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.location}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        biz_income = json.loads(self.biz_income)
        inventar = json.loads(self.inventar)
        obrok = json.loads(town[11])

        income = biz_income[f'{self.location}']

        tax_reg = {}
        tax_reg['рыба'] = round(income['рыба'] * (town[7] / 100))
        tax_reg['камень'] = round(income['камень'] * (town[7] / 100))
        tax_reg['дерево'] = round(income['дерево'] * (town[7] / 100))
        tax_reg['руда'] = round(income['руда'] * (town[7] / 100))
        tax_reg['хлопок'] = round(income['хлопок'] * (town[7] / 100))

        obrok['рыба'] += tax_reg['рыба']
        obrok['камень'] += tax_reg['камень']
        obrok['дерево'] += tax_reg['дерево']
        obrok['руда'] += tax_reg['руда']
        obrok['хлопок'] += tax_reg['хлопок']
        obrok['налог'] += income['налог']

        inventar['рыба'] += income['рыба'] - tax_reg['рыба']
        inventar['камень'] += income['камень'] - tax_reg['камень']
        inventar['дерево'] += income['дерево'] - tax_reg['дерево']
        inventar['руда'] += income['руда'] - tax_reg['руда']
        inventar['хлопок'] += income['хлопок'] - tax_reg['хлопок']

        price_harv = income['налог'] + income['зарплата']

        if self.cash < price_harv:
            await self.send_message(self.vk_id, f"Вы не можете забрать ресурсы, пока не выплатите зарплаты и налог на общую сумму в {price_harv} серебра.")
            return

        self.cash -= price_harv

        await self.send_message(self.vk_id, f"Вы собрали:\n"
                                     f"Рыба: {biz_income[f'{self.location}']['рыба']} шт. из них {tax_reg['рыба']} шт. ушло в оброк.\n"
                                     f"Камень: {biz_income[f'{self.location}']['камень']} шт. из них {tax_reg['камень']} шт. ушло в оброк.\n"
                                     f"Дерево: {biz_income[f'{self.location}']['дерево']} шт. из них {tax_reg['дерево']} шт. ушло в оброк.\n"
                                     f"Руда: {biz_income[f'{self.location}']['руда']} шт. из них {tax_reg['руда']} шт. ушло в оброк.\n"
                                     f"Хлопок: {biz_income[f'{self.location}']['хлопок']} шт. из них {tax_reg['хлопок']} шт. ушло в оброк.\n"
                                     f"\nВы заплатили {biz_income[f'{self.location}']['зарплата']} серебра рабочим и {biz_income[f'{self.location}']['налог']} серебра налога.")

        biz_income[f'{self.location}']['рыба'] = 0
        biz_income[f'{self.location}']['камень'] = 0
        biz_income[f'{self.location}']['дерево'] = 0
        biz_income[f'{self.location}']['руда'] = 0
        biz_income[f'{self.location}']['хлопок'] = 0
        biz_income[f'{self.location}']['налог'] = 0
        biz_income[f'{self.location}']['зарплата'] = 0

        inventar = json.dumps(inventar, ensure_ascii=False)
        obrok = json.dumps(obrok, ensure_ascii=False)
        biz_income = json.dumps(biz_income, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Users SET cash = {self.cash}, biz_income = '{biz_income}', inventar = '{inventar}' WHERE bot_id = {self.bot_id}")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Towns SET obrok = '{obrok}' WHERE name = '{self.location}'")
        await connection.commit()
        await command.close()
        await connection.close()



class Region:

    def __init__(self, name):
        self.name = name
        self.roads = 'Нет'
        self.town = 'Нет'
        self.owner = 0
        self.stone = 0
        self.tree = 0
        self.ore = 0
        self.silk = 0
        self.fish = 0

    async def add_region(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute("INSERT INTO Regions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
        self.name, self.roads, self.town, self.stone, self.tree, self.ore, self.silk, self.fish))
        await connection.commit()
        await command.close()
        await connection.close()
    async def load(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.name}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        self.name = result[0]
        self.roads = result[1]
        self.stone = result[2]
        self.tree = result[3]
        self.ore = result[4]
        self.silk = result[5]
        self.fish = result[6]
    async def add_road_output(self, target, distance):

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{target}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        if (result[1] == 'Нет'):
            js = json.dumps({})
        else:
            js = result[1]

        roads = json.loads(js)
        roads[self.name] = distance
        roads = json.dumps(roads, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Regions SET roads = '{roads}' WHERE name = '{target}'")
        await connection.commit()
        await command.close()
        await connection.close()
    async def add_road(self, target, distance):

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{self.name}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        if (result[1] == 'Нет'):
            js = json.dumps({})
        else:
            js = result[1]

        roads = json.loads(js)
        roads[target] = distance
        roads = json.dumps(roads, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Regions SET roads = '{roads}' WHERE name = '{self.name}'")
        await connection.commit()
        await command.close()
        await connection.close()

        await Region.add_road_output(self, target, distance)
    async def regeneration_res(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Regions SET stone = stone + inc_stone, tree = tree + inc_tree, ore = ore + inc_ore, silk = silk + inc_silk, fish = fish + inc_fish WHERE name = '{self.name}'")
        await connection.commit()
        await command.close()
        await connection.close()

class Town:

    def __init__(self, name):
        self.name = name
        self.population = 0
        self.location = 0
        self.market = json.dumps({
            'Еда': 0,
            'Камень': 0,
            'Руда': 0,
            'Дерево': 0,
            'Ткань': 0
        }, ensure_ascii=False)
        self.tax_pop = 0
        self.tax_reg = 0
        self.tax_land = 0
        self.tax_recruit = 0
        self.king = 0
        self.garnizon = 0
        self.specialization = json.dumps({
            "1":'рыба',
            "2":'хлопок'
        }, ensure_ascii=False)

    async def add_town(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute("INSERT INTO Towns VALUES (?, ?, ?)",
                                           (self.name, self.population, self.location))
        await connection.commit()
        await command.close()
        await connection.close()
    async def load(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{self.name}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        self.population = result[1]
        self.location = result[2]
        self.king = result[3]
        self.market = result[4]
        self.tax_pop = result[5]
        self.tax_land = result[6]
        self.tax_reg = result[7]
        self.tax_recruit = result[8]
        self.garnizon = result[9]
        self.specialization = result[10]
    async def consumption_res(self):

        market = json.loads(self.market)
        garnizon = json.loads(self.garnizon)

        consumption_stone = self.population * setting.cons_stone / 360 # Житель потребляет 0.08 ед. в год
        consumption_ore = self.population * setting.cons_ore / 360 # Житель потребляет 0.04 ед. в год
        consumption_tree = self.population * setting.cons_tree / 360 # Житель потребляет 0.16 ед. в год
        consumption_silk = self.population * setting.cons_silk / 360 # Житель потребляет 0.16 ед. в год
        consumption_fish = self.population * setting.cons_fish / 360 # Житель потребляет 0.48 ед. в год

        # Житель потребляет:
        # Еда: 480|0.48 ед.    # Стандарт цена: 60 # Достаток цена: 40 # Изобилие цена: 15
        # Хлопок: 160|0.16 ед. # Стандарт цена: 180 # Достаток цена: 120 # Изобилие цена: 45
        # Дерево: 160|0.16 ед. # Стандарт цена: 120 # Достаток цена: 80 # Изобилие цена: 30
        # Камень: 80|0.08 ед. # Стандарт цена: 180 # Достаток цена: 120 # Изобилие цена: 45
        # Руда: 40|0.04 ед.   # Стандарт цена: 300 # Достаток цена: 200 # Изобилие цена: 75
        #
        # Бюджет горожан   # Стандарт: 120

        # Рыба биз:
        # Производит 960 за год. В деньги стандарт 57600, Достаток 38400, Изобилие 14400
        # Стоимость:
        #
        #
        #
        #
        market['Цена']['камень'] = setting.price_standart_stone
        market['Цена']['руда'] = setting.price_standart_ore
        market['Цена']['дерево'] = setting.price_standart_tree
        market['Цена']['хлопок'] = setting.price_standart_silk
        market['Цена']['рыба'] = setting.price_standart_fish

        stone_mod = 0.01
        ore_mod = 0.01
        tree_mod = 0.02
        silk_mod = 0.02
        fish_mod = 0.05

        if market['Склад']['камень'] < 0:
            market['Склад']['камень'] = 0
            stone_mod = -0.01
            market['Цена']['камень'] = setting.price_deficit_stone
        if market['Склад']['камень'] > consumption_stone * 360:
            stone_mod += 0.01
            consumption_stone = consumption_stone * 1.1
            market['Цена']['камень'] = setting.price_dostatok_stone
        if market['Склад']['камень'] > consumption_stone * 360 * 3:
            stone_mod += 0.01
            consumption_stone = consumption_stone * 1.2
            market['Цена']['камень'] = setting.price_izobilie_stone

        if market['Склад']['руда'] < 0:
            market['Склад']['руда'] = 0
            ore_mod = -0.01
            market['Цена']['руда'] = setting.price_deficit_ore
        if market['Склад']['руда'] > consumption_ore * 360:
            ore_mod += 0.01
            consumption_ore = consumption_ore * 1.1
            market['Цена']['руда'] = setting.price_dostatok_ore
        if market['Склад']['руда'] > consumption_ore * 360 * 3:
            ore_mod += 0.01
            consumption_ore = consumption_ore * 1.1
            market['Цена']['руда'] = setting.price_izobilie_ore

        if market['Склад']['дерево'] < 0:
            market['Склад']['дерево'] = 0
            tree_mod = -0.02
            market['Цена']['дерево'] = setting.price_deficit_tree
        if market['Склад']['дерево'] > consumption_tree * 360:
            tree_mod += 0.02
            consumption_tree = consumption_tree * 1.1
            market['Цена']['дерево'] = setting.price_dostatok_tree
        if market['Склад']['дерево'] > consumption_tree * 360 * 3:
            tree_mod += 0.02
            consumption_tree = consumption_tree * 1.1
            market['Цена']['дерево'] = setting.price_izobilie_tree

        if market['Склад']['хлопок'] < 0:
            market['Склад']['хлопок'] = 0
            silk_mod = -0.02
            market['Цена']['хлопок'] = setting.price_deficit_silk
        if market['Склад']['хлопок'] > consumption_silk * 360:
            silk_mod += 0.02
            consumption_silk = consumption_silk * 1.1
            market['Цена']['хлопок'] = setting.price_dostatok_silk
        if market['Склад']['хлопок'] > consumption_silk * 360 * 3:
            silk_mod += 0.02
            consumption_silk = consumption_silk * 1.1
            market['Цена']['хлопок'] = setting.price_izobilie_silk

        if market['Склад']['рыба'] < 0:
            market['Склад']['рыба'] = 0
            fish_mod = -0.15
            market['Цена']['рыба'] = setting.price_deficit_fish
        if market['Склад']['рыба'] > consumption_fish * 360:
            fish_mod += 0.05
            consumption_fish = consumption_fish * 1.1
            market['Цена']['рыба'] = setting.price_dostatok_fish
        if market['Склад']['рыба'] > consumption_fish * 360 * 3:
            fish_mod += 0.05
            consumption_fish = consumption_fish * 1.1
            market['Цена']['рыба'] = setting.price_izobilie_fish

        consumption_stone = round(consumption_stone)
        consumption_ore = round(consumption_ore)
        consumption_tree = round(consumption_tree)
        consumption_silk = round(consumption_silk)
        consumption_fish = round(consumption_fish)

        market['Склад']['камень'] -= consumption_stone
        market['Склад']['руда'] -= consumption_ore
        market['Склад']['дерево'] -= consumption_tree
        market['Склад']['хлопок'] -= consumption_silk
        market['Склад']['рыба'] -= consumption_fish

        tax_money = round((self.population * setting.income_npc * (self.tax_pop / 100)) / 360)
        tax_recruit = round((self.population * (self.tax_recruit / 100)) / 360)
        garnizon['рекруты'] += tax_recruit
        modificator = round(fish_mod + stone_mod + silk_mod + tree_mod + ore_mod, 2)
        income = 1 - (self.tax_pop / 100) - (self.tax_recruit / 100) + modificator

        income = (self.population * income - self.population) / 360

        self.population = round(self.population + income)

        await User.send_message(User,setting.log_id, text=f"Город: {self.name}\nНаселение:{self.population}\nПрирост: {round((1 - income) * -100, 2)}\nСобранный налог[{self.tax_pop}%]: {tax_money}\nРекрутировано[{self.tax_recruit}%]: {tax_recruit}\nМодификатор ресурсов: {round(modificator * 100)}%\nПотребление:\n[{market['Склад']['камень']}]Камень: {consumption_stone}\n[{market['Склад']['руда']}]Руда:{consumption_ore}\n[{market['Склад']['дерево']}]Дерево:{consumption_tree}\n[{market['Склад']['хлопок']}]Хлопок:{consumption_silk}\n[{market['Склад']['рыба']}]Рыба:{consumption_fish}\n")

        market = json.dumps(market, ensure_ascii=False)
        garnizon = json.dumps(garnizon, ensure_ascii=False)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(
            f"UPDATE Towns SET market = '{market}', garnizon = '{garnizon}', population = {self.population} WHERE name = '{self.name}'")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(
            f"UPDATE Users SET cash = cash + {tax_money} WHERE bot_id = {self.king}")
        await connection.commit()
        await command.close()
        await connection.close()
    async def last_insert_biz(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT MAX(id) FROM Bisisnes")
        result = await command.fetchone()
        await command.close()
        await connection.close()
        result = result[0]
        return result
    async def add_biz(self, id, type_biz, res, income, town, owner_id, owner_name, payment):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute("INSERT INTO Bisisnes VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, type_biz, res, income, town, owner_id, owner_name, payment))
        await connection.commit()
        await command.close()
    async def create_biz(self, bot_id, type_biz):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Users WHERE bot_id = '{bot_id}'")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        market = json.loads(self.market)
        price = 0

        if type_biz == "Рыб.Судно":
            count_tree = setting.price['Рыб.Судно']['дерево']
            count_silk = setting.price['Рыб.Судно']['хлопок']
            count_worker = setting.price['Рыб.Судно']['работа']

            if market['Склад']['дерево'] < count_tree:
                await User.send_message(User,result[2],f"На рынке не хватает дерева для постройки судна.[{count_tree} шт.]")
                return
            if market['Склад']['хлопок'] < count_silk:
                await User.send_message(User,result[2],f"На рынке не хватает хлопка для постройки судна.[{count_silk} шт.]")
                return
            price = market['Цена']['дерево'] * count_tree + market['Цена']['хлопок'] * count_silk + count_worker
            if result[3] < price:
                await User.send_message(User,result[2],f"У вас недостаточно денег. [{price} сер.]")
                return

            js_task = {
                "vk_id": result[2],
                "ресурс": 'рыба',
                "тип бизнеса": 'Рыб.Судно',
                "доход": setting.price['Рыб.Судно']['доход'],
                "город": result[6],
                "bot_id": result[0],
                "name": result[1],
                "зарплата": setting.price['Рыб.Судно']['зарплата']
            }
            js_task = json.dumps(js_task, ensure_ascii=False)
            data = 1
            await defs.create_task('Постройка бизнеса', js_task, data)

            market['Склад']['дерево'] -= count_tree
            market['Склад']['хлопок'] -= count_silk

            await User.send_message(User,result[2],f"Вы начали постройку рыболовного судна, заплатив {price} серебра.")

        if type_biz == "Плантация хлопка":
            count_tree = setting.price['Плантация хлопка']['дерево']
            count_silk = setting.price['Плантация хлопка']['хлопок']
            price_worker = setting.price['Плантация хлопка']['работа']

            if int(market['Склад']['дерево']) < count_tree:
                await User.send_message(User,result[2],f"На рынке не хватает дерева для постройки плантации.[{count_tree} шт.]")
                return
            if market['Склад']['хлопок'] < count_silk:
                await User.send_message(User,result[2],f"На рынке не хватает хлопка для постройки плантации.[{count_silk} шт.]")
                return
            price =  market['Цена']['дерево'] * count_tree + market['Цена']['хлопок'] * count_silk + price_worker
            if result[3] < price:
                await User.send_message(User,result[2],f"У вас недостаточно денег. [{price} сер.]")
                return

            js_task = {
                "vk_id": result[2],
                "ресурс": 'хлопок',
                "тип бизнеса": 'Плантация хлопка',
                "доход": setting.price['Плантация хлопка']['доход'],
                "город": result[6],
                "bot_id": result[0],
                "name": result[1],
                "зарплата": setting.price['Плантация хлопка']['зарплата']
            }
            js_task = json.dumps(js_task, ensure_ascii=False)
            data = 1
            await defs.create_task('Постройка бизнеса', js_task, data)

            market['Склад']['дерево'] -= count_tree
            market['Склад']['хлопок'] -= count_silk

            await User.send_message(User,result[2],f"Вы начали постройку плантации, заплатив {price} серебра.")
        if type_biz == "Лесопилка":
            count_tree = setting.price['Лесопилка']['дерево']
            count_silk = setting.price['Лесопилка']['хлопок']
            count_stone = setting.price['Лесопилка']['камень']
            count_ore = setting.price['Лесопилка']['руда']
            price_worker = setting.price['Лесопилка']['работа']

            if market['Склад']['дерево'] < count_tree:
                await User.send_message(User,result[2],f"На рынке не хватает дерева для постройки лесопилки.[{count_tree} шт.]")
                return
            if market['Склад']['хлопок'] < count_silk:
                await User.send_message(User,result[2],f"На рынке не хватает хлопка для постройки лесопилки.[{count_silk} шт.]")
                return
            if market['Склад']['камень'] < count_stone:
                await User.send_message(User,result[2],f"На рынке не хватает камня для постройки лесопилки.[{count_stone} шт.]")
                return
            if market['Склад']['руда'] < count_ore:
                await User.send_message(User,result[2],f"На рынке не хватает руды для постройки лесопилки.[{count_stone} шт.]")
                return
            price = count_ore * market['Цена']['руда'] + count_stone * market['Цена']['камень'] + market['Цена']['дерево'] * count_tree + market['Цена']['хлопок'] * count_silk + price_worker
            if result[3] < price:
                await User.send_message(User,result[2],f"У вас недостаточно денег. [{price} сер.]")
                return

            js_task = {
                "vk_id": result[2],
                "ресурс": 'дерево',
                "тип бизнеса": 'Лесопилка',
                "доход": setting.price['Лесопилка']['доход'],
                "город": result[6],
                "bot_id": result[0],
                "name": result[1],
                "зарплата": setting.price['Лесопилка']['зарплата']
            }
            js_task = json.dumps(js_task, ensure_ascii=False)
            data = 1
            await defs.create_task('Постройка бизнеса', js_task, data)

            market['Склад']['дерево'] -= count_tree
            market['Склад']['хлопок'] -= count_silk
            market['Склад']['камень'] -= count_stone
            market['Склад']['руда'] -= count_ore

            await User.send_message(User,result[2],f"Вы начали постройку лесопилки, заплатив {price} серебра.")
        if type_biz == "Каменоломня":
            count_tree = setting.price['Каменоломня']['дерево']
            count_silk = setting.price['Каменоломня']['хлопок']
            count_stone = setting.price['Каменоломня']['камень']
            count_ore = setting.price['Каменоломня']['руда']
            price_worker = setting.price['Каменоломня']['работа']

            if market['Склад']['дерево'] < count_tree:
                await User.send_message(User,result[2],f"На рынке не хватает дерева для постройки каменоломни.[{count_tree} шт.]")
                return
            if market['Склад']['хлопок'] < count_silk:
                await User.send_message(User,result[2],f"На рынке не хватает хлопка для постройки каменоломни.[{count_silk} шт.]")
                return
            if market['Склад']['камень'] < count_stone:
                await User.send_message(User,result[2],f"На рынке не хватает камня для постройки каменоломни.[{count_stone} шт.]")
                return
            if market['Склад']['руда'] < count_stone:
                await User.send_message(User,result[2],f"На рынке не хватает руды для постройки каменоломни.[{count_stone} шт.]")
                return
            price = count_ore * market['Цена']['руда'] + count_stone * market['Цена']['камень'] + market['Цена']['дерево'] * count_tree + market['Цена']['хлопок'] * count_silk + price_worker
            if result[3] < price:
                await User.send_message(User,result[2],f"У вас недостаточно денег. [{price} сер.]")
                return

            js_task = {
                "vk_id": result[2],
                "ресурс": 'камень',
                "тип бизнеса": 'Каменоломня',
                "доход": setting.price['Каменоломня']['доход'],
                "город": result[6],
                "bot_id": result[0],
                "name": result[1],
                "зарплата": setting.price['Каменоломня']['зарплата']
            }
            js_task = json.dumps(js_task, ensure_ascii=False)
            data = 1
            await defs.create_task('Постройка бизнеса', js_task, data)

            market['Склад']['дерево'] -= count_tree
            market['Склад']['хлопок'] -= count_silk
            market['Склад']['камень'] -= count_stone
            market['Склад']['руда'] -= count_ore

            await User.send_message(User,result[2],f"Вы начали постройку рыболовного каменоломни, заплатив {price} серебра.")

        if type_biz == "Шахта":
            count_tree = setting.price['Шахта']['дерево']
            count_silk = setting.price['Шахта']['хлопок']
            count_stone = setting.price['Шахта']['камень']
            count_ore = setting.price['Шахта']['руда']
            price_worker = setting.price['Шахта']['работа']

            if market['Склад']['руда'] < count_ore:
                await User.send_message(User,result[2],f"На рынке не хватает руды для постройки шахты.[{count_tree} шт.]")
                return
            if market['Склад']['дерево'] < count_tree:
                await User.send_message(User,result[2],f"На рынке не хватает дерева для постройки шахты.[{count_tree} шт.]")
                return
            if market['Склад']['хлопок'] < count_silk:
                await User.send_message(User,result[2],f"На рынке не хватает хлопка для постройки шахты.[{count_silk} шт.]")
                return
            if market['Склад']['камень'] < count_stone:
                await User.send_message(User,result[2],f"На рынке не хватает камня для постройки шахты.[{count_stone} шт.]")
                return
            price = count_ore * market['Цена']['руда'] + count_stone * market['Цена']['камень'] + market['Цена']['дерево'] * count_tree + market['Цена']['хлопок'] * count_silk + price_worker
            if result[3] < price:
                await User.send_message(User,result[2],f"У вас недостаточно денег. [{price} сер.]")
                return

            js_task = {
                "vk_id": result[2],
                "ресурс": 'руда',
                "тип бизнеса": 'Шахта',
                "доход": setting.price['Шахта']['доход'],
                "город": result[6],
                "bot_id": result[0],
                "name": result[1],
                "зарплата": setting.price['Шахта']['зарплата']
            }
            js_task = json.dumps(js_task, ensure_ascii=False)
            data = 1
            await defs.create_task('Постройка бизнеса', js_task, data)

            market['Склад']['дерево'] -= count_tree
            market['Склад']['хлопок'] -= count_silk
            market['Склад']['камень'] -= count_stone
            market['Склад']['руда'] -= count_ore

            await User.send_message(User,result[2],f"Вы начали постройку шахты, заплатив {price} серебра.")

        market = json.dumps(market, ensure_ascii=False)
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(
            f"UPDATE Users SET cash = cash - {price} WHERE bot_id = {self.king}")
        await connection.commit()
        await command.close()
        await connection.close()

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(
            f"UPDATE Towns SET market = '{market}' WHERE name = '{self.name}'")
        await connection.commit()
        await command.close()
        await connection.close()

class Post:

    def __init__(self, id):
        self.id = id
        self.likers_ids = json.dumps({})
        self.reply_ids = json.dumps({})
        self.data = time.time()
        self.avtor = '0'
        self.payload = '0'

    async def add_post(self, avtor, payload):
        self.avtor = int(avtor)
        self.payload = str(payload)
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute("INSERT INTO Posts VALUES (?, ?, ?, ?, ?, ?)", (
        self.id, self.avtor, self.payload, self.likers_ids, self.reply_ids, self.data))
        await connection.commit()
        await command.close()
        await connection.close()
    async def load(self):
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Posts WHERE id = {self.id}")
        result = await command.fetchone()
        await command.close()
        await connection.close()

        self.id = result[0]
        self.avtor = result[1]
        self.payload = result[2]
        self.likers_ids = result[3]
        self.reply_ids = result[4]
        self.data = result[5]
    async def add_reply(self, replyer_id):
        reply_ids = json.loads(self.reply_ids)
        reply_ids[replyer_id] = replyer_id
        reply_ids = json.dumps(reply_ids)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Posts SET reply_ids = ? WHERE id = ?", (reply_ids, self.id))
        await connection.commit()
        await command.close()
        await connection.close()
    async def add_like(self, liker_id):
        likers_ids = json.loads(self.likers_ids)
        likers_ids[liker_id] = liker_id
        likers_ids = json.dumps(likers_ids)

        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"UPDATE Posts SET liker_ids = ? WHERE id = ?", (likers_ids, self.id))
        await connection.commit()
        await command.close()
        await connection.close()
