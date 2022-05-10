import aiosqlite, setting

def replace_name(name):
    name = name.replace('_',' ')
    return name

async def give_cash(bot_id, count):
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"UPDATE Users SET cash = cash + {count} WHERE bot_id = {bot_id}")
    await connection.commit()
    await command.close()
    await connection.close()

async def tp_user(bot_id, loc):
    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"UPDATE Users SET location = '{loc}' WHERE bot_id = {bot_id}")
    await connection.commit()
    await command.close()
    await connection.close()

async def type_of_loc(name):
    try:
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Towns WHERE name = '{name}'")
        town = await command.fetchone()
        await command.close()
        await connection.close()

        if town != None:
            loc_is = 'Town'
            return loc_is
    except: loc_is = 'Ошибка'

    try:
        connection = await aiosqlite.connect(setting.db)
        command = await connection.execute(f"SELECT * FROM Regions WHERE name = '{name}'")
        reg = await command.fetchone()
        await command.close()
        await connection.close()

        if reg != None:
            loc_is = 'Region'
            return loc_is
    except: loc_is = 'Ошибка'


async def create_task(type_task, js_task, data):

    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute(f"SELECT MAX(id) FROM Tasks")
    result = await command.fetchone()
    await command.close()
    await connection.close()
    res = result[0] + 1

    connection = await aiosqlite.connect(setting.db)
    command = await connection.execute("INSERT INTO Tasks VALUES (?, ?, ?, ?)", (res, type_task, js_task, data))
    await connection.commit()
    await command.close()


async def sum_army_hp(army):
    hp_1 = army['ополченец'] * setting.price['ополченец']['хп']
    hp_2 = army['стрелок'] * setting.price['стрелок']['хп']
    hp_3 = army['всадник'] * setting.price['всадник']['хп']
    hp_4 = army['воин'] * setting.price['воин']['хп']
    hp_5 = army['наемный стрелок'] * setting.price['наемный стрелок']['хп']
    hp_6 = army['наемный всадник'] * setting.price['наемный всадник']['хп']
    hp_7 = army['наемный воин'] * setting.price['наемный воин']['хп']

    hp = hp_1 + hp_2 + hp_3 + hp_4 + hp_5 + hp_6 + hp_7

    try:
        median = {
            'ополченец': round(hp_1 / (hp / 100), 2),
            'стрелок': round(hp_2 / (hp / 100), 2),
            'всадник': round(hp_3 / (hp / 100), 2),
            'воин': round(hp_4 / (hp / 100), 2),
            'наемный стрелок': round(hp_5 / (hp / 100), 2),
            'наемный всадник': round(hp_6 / (hp / 100), 2),
            'наемный воин': round(hp_7 / (hp / 100), 2)
        }
    except:
        median = {
            'ополченец': 100,
            'стрелок': 100,
            'всадник': 100,
            'воин': 100,
            'наемный стрелок': 100,
            'наемный всадник': 100,
            'наемный воин': 100
        }
    return hp, median

async def sum_army_dd(army):
    dd = 0
    dd += army['ополченец'] * setting.price['ополченец']['урон']
    dd += army['стрелок'] * setting.price['стрелок']['урон']
    dd += army['всадник'] * setting.price['всадник']['урон']
    dd += army['воин'] * setting.price['воин']['урон']
    dd += army['наемный стрелок'] * setting.price['наемный стрелок']['урон']
    dd += army['наемный всадник'] * setting.price['наемный всадник']['урон']
    dd += army['наемный воин'] * setting.price['наемный воин']['урон']
    return dd

async def fight(army_attack, army_defense):

    hp_army_attack, md_army_attack = await sum_army_hp(army_attack)
    dd_army_attack = await sum_army_dd(army_attack)

    hp_army_defense, md_army_defense = await sum_army_hp(army_defense)
    dd_army_defense = await sum_army_dd(army_defense)

    army_attack['ополченец'] = round(((setting.price['ополченец']['хп'] * army_attack['ополченец']) - (dd_army_defense / 100 * md_army_attack['ополченец'])) / setting.price['ополченец']['хп'])
    army_attack['стрелок'] = round(((setting.price['стрелок']['хп'] * army_attack['стрелок']) - (dd_army_defense / 100 * md_army_attack['стрелок'])) / setting.price['стрелок']['хп'])
    army_attack['всадник'] = round(((setting.price['всадник']['хп'] * army_attack['всадник']) - (dd_army_defense / 100 * md_army_attack['всадник'])) / setting.price['всадник']['хп'])
    army_attack['воин'] = round(((setting.price['воин']['хп'] * army_attack['воин']) - (dd_army_defense / 100 * md_army_attack['воин'])) / setting.price['воин']['хп'])
    army_attack['наемный стрелок'] = round(((setting.price['наемный стрелок']['хп'] * army_attack['наемный стрелок']) - (dd_army_defense / 100 * md_army_attack['наемный стрелок'])) / setting.price['наемный стрелок']['хп'])
    army_attack['наемный всадник'] = round(((setting.price['наемный всадник']['хп'] * army_attack['наемный всадник']) - (dd_army_defense / 100 * md_army_attack['наемный всадник'])) / setting.price['наемный всадник']['хп'])
    army_attack['наемный воин'] = round(((setting.price['наемный воин']['хп'] * army_attack['наемный воин']) - (dd_army_defense / 100 * md_army_attack['наемный воин'])) / setting.price['наемный воин']['хп'])

    army_defense['ополченец'] = round(((setting.price['ополченец']['хп'] * army_defense['ополченец']) - (dd_army_attack / 100 * md_army_defense['ополченец'])) / setting.price['ополченец']['хп'])
    army_defense['стрелок'] = round(((setting.price['стрелок']['хп'] * army_defense['стрелок']) - (dd_army_attack / 100 * md_army_defense['стрелок'])) / setting.price['стрелок']['хп'])
    army_defense['всадник'] = round(((setting.price['всадник']['хп'] * army_defense['всадник']) - (dd_army_attack / 100 * md_army_defense['всадник'])) / setting.price['всадник']['хп'])
    army_defense['воин'] = round(((setting.price['воин']['хп'] * army_defense['воин']) - (dd_army_attack / 100 * md_army_defense['воин'])) / setting.price['воин']['хп'])
    army_defense['наемный стрелок'] = round(((setting.price['наемный стрелок']['хп'] * army_defense['наемный стрелок']) - (dd_army_attack / 100 * md_army_defense['наемный стрелок'])) / setting.price['наемный стрелок']['хп'])
    army_defense['наемный всадник'] = round(((setting.price['наемный всадник']['хп'] * army_defense['наемный всадник']) - (dd_army_attack / 100 * md_army_defense['наемный всадник'])) / setting.price['наемный всадник']['хп'])
    army_defense['наемный воин'] = round(((setting.price['наемный воин']['хп'] * army_defense['наемный воин']) - (dd_army_attack / 100 * md_army_defense['наемный воин'])) / setting.price['наемный воин']['хп'])

    return army_attack, army_defense
