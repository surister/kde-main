from Bot.KDE.json_commands import read_db


def total_registered_users(steam=False):
    y, u = 0, 0
    x = read_db()

    for keys, value in x.items():
        if not value['ok']:
            y += 1
        elif value['ok']:
            u += 1
    return y, u, len(x.keys())

