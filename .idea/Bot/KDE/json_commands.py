import json


def read_db():

    with open('database.json', 'r') as db:
        x = json.load(db)
    db.close()
    return x


def mod_update(author, to_update, new_info):
    a = read_db()
    a[author][to_update] = new_info
    with open('database.json', "w") as db:
        json.dump(a, db,  indent=3)
    db.close()


def update_db(info=None, author=None, steam=None):
    if not steam:
        a = read_db()
        a[author] = info
        with open('database.json', "w") as db:
            json.dump(a, db, indent=3)
        db.close()

    else:
        a = read_db()
        a[author]["steam_id"] = steam
        with open('database.json', "w") as db:
            json.dump(a, db, indent=3)
        db.close()


def read_arg(user, arg):
    with open('database.json', 'r') as db:
        x = json.load(db)
        db.close()
        return x[user][arg]


def read_all(user):
    try:
        with open('database.json', 'r') as db:
            x = json.load(db)
            db.close()
            return x[user]
    except KeyError:
        return 'Este usuario no existe en la base de datos'


def get_json():
    with open('database.json', 'r') as db:
        x = json.load(db)
        db.close()
        return x


def str_to_dic(message):
    json_acceptable_string = message.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    return d


def check_duplicity(ide):
    x = read_db()
    for i in x.values():
        if ide == i['steam_id']:
            return True
    return False

