from time import time

from discord import Game
from discord.ext.commands import Bot

from Bot.KDE.constants import __version__

Bot = Bot(command_prefix='!')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    await Bot.change_presence(game=Game(name="Ark Survival Evolved"))
    before = time()

    a = Bot.get_channel('461112442185973760')
    b = await Bot.get_message(a, '461136423345586186')
    Bot.messages.append(b)

    after = time()
    s = '\n----------------------------\n'
    fmt = "--v:" + __version__ + "\nConectado como: {0} \n Id: {1} \n It took to init the bot {2}".format(Bot.user.name,
                                                                                                          Bot.user.id,
                                                                                                          after - before)
    print(s, fmt, s)


sur = "NDQ2NzE4NDAzMjk0NTI3NDk5.DgMFLA.HTKDaxMMwUaRS49D4znianopPBk"
kde = "NDYwODQ5OTMzMTE3ODE2ODQ3.DhKw-A.ZktmEN8cITd_4RkJ340eTmyXWFg"

startup_extensions = ["cogs.commands", "cogs.events", "cogs.tickets", "cogs.test"]

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            Bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

Bot.run(kde, reconnect=True)

# TODO Mejorar mensaje steam registro --
# Solucionar gif --
# TODO Sistema de tickets
""" Inicio de ticket, el usuario manda un ticket en un canal donde estan las instrucciones y comendaciones
# hay 5 tipos de tickets, {1: "Reporte de bug",
#                       2: "Reporte de Usuario",
#                       3: "Necesidad de asistencia especial",
#                       4: "Reporte de abuso, cheat o hack",
#                       5: "Sugerencia"
#                       }
# --
Todo 3
No tiene porque ser asi de estricto, simplemente es para que nosotros al ver simplemente el numero sepamos de que va 
mas o menos la cosa.

Nosotros recibimos ese mensaje en un canal de tickets, donde al escribir algo por el estilo !abrir {codigo de ticket}
empezamos una sesion con ese usuario, donde el bot le hablara por privado todo lo que nosotros le digamos (a su vez si el usuario nos dice algo el mensaje se editara
añadiendo la información de dicho usuario) hasta que consideremos la ayuda como terminada y hagamos algo en plan !cerrar {codigo de ticket} donde el ticket y todo lo hablado
se almacenara en formato json

#TODO Comando !ayuda muestre la lista de comandos dependiendo del idioma del usuario que lo usa
# ?? posiblemente no."""
