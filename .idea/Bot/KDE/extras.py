from Bot.KDE.json_commands import read_db
import random


def get_attacked_users(attack_dic: list, json_db: dict):

    x = []

    for user in attack_dic:
        for discord_id in json_db:
            if json_db[discord_id]['steam_id'] == int(user):
                x.append(discord_id)
    return x


def server_wh(wh_msg):
    return tuple((wh_msg.keys()))[0]


def switcher_wh(wh_msg):
    return tuple(wh_msg[tuple((wh_msg.keys()))[0]].keys())[0]


def info_switcher_wh(wh_msg):
    return wh_msg[tuple(wh_msg.keys())[0]][tuple(wh_msg[tuple(wh_msg.keys())[0]].keys())[0]]


def players_wh(wh_msg):
    return wh_msg[tuple(wh_msg.keys())[0]][tuple(wh_msg[tuple(wh_msg.keys())[0]].keys())[1]]


def total_registered_users():
    y = u = 0
    x = read_db()

    for keys, value in x.items():
        if not value['ok']:
            y += 1
        elif value['ok']:
            u += 1
    return 'No registro completo: ' + str(y), 'Registro completo: ' + str(u), 'Usuarios totales en db: ' + str(len(x.keys()))


def ticket_num_generator(languaje):
    test = [str(random.choice(list(range(10)))) for i in range(3)]
    return "".join(test)+languaje


