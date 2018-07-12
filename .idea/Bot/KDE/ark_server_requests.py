import requests
from requests_html import HTMLSession
from html.parser import HTMLParser
from Bot.KDE.constants import kde_servers


def main(server: str):
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
        listerino.append(f' Server vacio')

    return listerino


def cant_jugadores():
    x = []
    b = []
    c = []
    for i in kde_servers.values():
        for k in main(i):
            x.append(k)
    for p in x:
        if "Online Players" in p:
            b.append(p)
    for l in b:
        for o in l:
            try:
                if isinstance(int(o), int):
                    c.append(int(o))
            except:
                pass
    return sum(c)

