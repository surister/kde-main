import requests
from requests_html import HTMLSession
from html.parser import HTMLParser

from Bot.KDE.constants import kde_servers


def main(server: str, status=False):
    def ark_users(ser):
        r = requests.get(ser)
        r_type, r_encode = r.headers['content-type'].split("; ")

        if r_type == "text/html":
            session = HTMLSession()
            v = session.get(ser)
            return v.text
# ---------------------

    class MyHTMLParser(HTMLParser):
        container = {}
        counter = 0

        def handle_data(self, data):
            data_to_add = data.strip('\n').strip('\t').strip('')
            if data_to_add != "":
                MyHTMLParser.container[MyHTMLParser.counter] = data_to_add
                MyHTMLParser.counter += 1
            return MyHTMLParser.container

    parser = MyHTMLParser()

    parser.feed(ark_users(server))

    if status:
        return f'Server {list(kde_servers.keys())[list(kde_servers.values()).index(server)]} status -> ' \
               f'{parser.container[97]}'
    else:
        for key, value in list(parser.container.items()):
            if 'Online Players' in value:
                a = key
            elif 'Other Servers' in value:
                b = key
        listerino = []
        k = 0
        try:
            for i in range(b-a):
                listerino.append(parser.container[a+k])
                k += 1
        except UnboundLocalError:
            listerino.append(f'Server vacio')

        return listerino


def cant_jugadores():
    x = []
    b = []

    for i in kde_servers.values():
        for k in main(i):
            x.append(k)
    for p in x:
        if "Online Players" in p:
            b.append(p)
    c = " ".join(b)

    return sum([int(s) for s in c.split() if s.isdigit()])


def server_check():
    x = []
    for i in kde_servers.values():
        for k in main(i):
            if 'Server vacio'in k or 'Online Players' in k:
                x.append(k)
