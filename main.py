import time
from time import time
from discord.ext.commands import Bot
from discord import Game
import discord

client = discord.Client()
Bot = Bot(command_prefix='!')


@Bot.event
async def on_ready():
    await Bot.change_presence(game=Game(name="Ark Survival Evolved"))
    before = time()
    Bot.remove_command('help')
    a = Bot.get_channel('461112442185973760')
    b = await Bot.get_message(a, '461136423345586186')
    Bot.messages.append(b)

    Bot.load_extension("commands")
    Bot.load_extension("events")
    after = time()
    total_time = after - before
    fmt = "Conectado como: {0} \n Id: {1} \n It took to init the bot {2}".format(Bot.user.name, Bot.user.id, total_time)
    print("----------------------------\n", fmt, "\n----------------------------\n")

Bot.run("NDYwODQ5OTMzMTE3ODE2ODQ3.DhKw-A.ZktmEN8cITd_4RkJ340eTmyXWFg")
# Si tiene - es que esta hecho.
# TODO Rangos y obtencion de inf básica
# 1. Entra el usuario
# 2. Tiene el rango new y solo puede ver el canal de welcome, donde tiene que elegir un idioma -
# 3. Una vez que elige un idioma, el bot le manda por privado el tema de steam en su idioma -
# 4. Comando de ayuda -
# 5. Comando de steam que guarde en json la informacion -
# 6. Una vez que manda el steam id, el bot le quita el rango de new y le pone el rango de su idioma -

# TODO ..
# 1. Chequeo que la id de steam este correctamente puesta -
# 2. Chequeo que la id de steam exista -
# 3. Añadir steam id al json -

# TODO Sistema de tickets
# ...
#TODO Comandos para el dia de ''apertura''
# quitar kde servers y poner new a todo el mundo

#TODO comando de basic info de servers para admins
# Comando estilo !info @surister <a conocer> -
# <a conocer -> lan = language, steam_id = steamid, ok = True/False -
#TODO Comando !ayuda muestre la lista de comandos dependiendo del idioma del usuario que lo usa
#
