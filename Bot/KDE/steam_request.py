import json
import requests


def id_parser(steam_url: str):

    if steam_url.startswith("https://steamcommunity.com/id/"):
        x = steam_url.replace("https://steamcommunity.com/id/", "")
        if x.endswith("/"):
            a = x.replace("/", "")
            return a
        elif x.endswith("/home"):
            a = x.replace("/home", "")
            return a
        return x

    elif steam_url.startswith("https://steamcommunity.com/profiles/"):
        x = steam_url.replace("https://steamcommunity.com/profiles/", "")
        if x.endswith("/"):
            a = x.replace("/", "")
            return a
        elif x.endswith("/home"):
            a = x.replace("/home", "")
            return a
        return x
    return steam_url


def steam_id_format_check(id_steam):
        return id_steam.isnumeric() and len(id_steam) == 17


def steam_64id(id_steam: str):
    if steam_id_format_check(id_steam):
        return int(id_steam)
    key = "F178A3511A0D8E8D5C6C5697250B5554"
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/" \
          "v1/?key={0}&vanityurl={1}".format(key, id_steam)
    response = requests.get(url)

    json_acceptable_string = response.text.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    if d['response']['success'] == 1:
        return int(d['response']['steamid'])
    return False
