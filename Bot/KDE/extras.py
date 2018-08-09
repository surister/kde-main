from Bot.KDE.json_commands import read_db, read_arg
import random


def get_attacked_users(attack_dic: list, json_db: dict):

    """Recibe una lista de steam ids, la database, y devuelve una lista con  los discord ids de de dichas steam ids """

    x = []

    for user in attack_dic:
        for discord_id in json_db:
            if json_db[discord_id]['steam_id'] == int(user):
                x.append(discord_id)
    return x


def server_wh(wh_msg):

    """Parsea el mensaje de la webhook y te devuelve el numero de server, puedes ver la estructura de cada webhook
    segun su switcher en constants.py"""

    return tuple((wh_msg.keys()))[0]


def switcher_wh(wh_msg):

    """Parsea el mensaje de la webhook y te devuelve el numero de switcher"""

    return tuple(wh_msg[tuple((wh_msg.keys()))[0]].keys())[0]


def info_switcher_wh(wh_msg):

    """Parsea la info dentro de {switcher : "info switcher"} y devuelve su value, siendo el switcher la key, la infor
    macion depende del tipo de switcher, excepto el nº6 que devuelve string, los demas son listas"""

    return wh_msg[tuple(wh_msg.keys())[0]][tuple(wh_msg[tuple(wh_msg.keys())[0]].keys())[0]]


def players_wh(wh_msg):

    """Parsea la info del webhook y devuelve la lista de jugadores que estan siendo atacados"""

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


def ticket_num_generator(language):
    test = [str(random.choice(list(range(10)))) for i in range(3)]
    return "".join(test) + language


def has_steam_id(user):

    """ Comprueba si el usuario tiene registrada su steam id en la base de datos, si es así devuelve la steam id, si no
    devuelve string"""

    x = read_db()
    if user in list(x.keys()):
        x = read_arg(user, 'steam_id')
        if x != "":
            return x
        return 'No tiene steam id'

