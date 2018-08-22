import asyncio

from time import strftime

from discord import Embed
from discord.ext.commands import Bot

from Bot.KDE.login import Login
from Bot.KDE.cogs_manager import load_cogs
from Bot.KDE.constants import status_channels, kde_servers
from Bot.KDE.ark_server_requests import main

bot = Bot(command_prefix='!')
bot.remove_command('help')


async def my_background_task():
    await bot.wait_until_ready()

    while not bot.is_closed:
        x = [f'{main(server, True)} :x:' if 'Offline' in main(server, True) else f'{main(server, True)} :o:' for server
             in kde_servers.values()]

        status = Embed(title='__**Server Status**__', )
        status.set_footer(text=f'Last check was -> {strftime("%c")}  - Every/Cada : 5 minutes')
        for new in x:
            status.add_field(name=new, value='\u200b', inline=False)

        for channel, message in status_channels.items():
            m = await bot.get_message(bot.get_channel(channel), message)
            await bot.edit_message(m, new_content='', embed=status)

        await asyncio.sleep(300)

if __name__ == "__main__":
    load_cogs(bot)
    bot.loop.create_task(my_background_task())
    bot.run(Login.kde)


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


# En definitiva faltan cosas por mejorar:
# Guardar steam - ids en vez de nombres (x dios surister)
# que cuando alguien se vaya del discord, se borre sus datos también de la base de datos
# SANEAR BASE DE DATOS - FUSIONARLA CON LA DE KDE, COMPROBAR LOS QUE YA NO ESTAN Y BORRARLOS PARA EVITAR ERRORES,
# MEJOR QUE BORRAR, guardar sus datos en base de datos secundaria como documento historico de admin etcetc
