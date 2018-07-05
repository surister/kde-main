import discord
from discord.ext import commands
from discord import Embed
from discord.utils import find

from asyncio import sleep
from time import strftime

from Bot.KDE.constants import *
from Bot.KDE.constants import _helpo
from Bot.KDE.json_commands import update_db, read_arg, str_to_dic, get_json
from Bot.KDE.extras import get_attacked_users


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.CommandNotFound):
            await self.bot.send_message(ctx.message.channel, "That command does not exist")
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.bot.send_message(ctx.message.channel, "Missing required argument")
        else:
            print(error)

    @staticmethod
    async def on_error(event):
        print(event)


class OnMessage:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.channel == self.bot.get_channel("462267741152346112"):
            a = str_to_dic(message.content)

            server = list(a.keys())[0]
            tribu_atacante = list(a[server].keys())[0]
            atacador = a[server][tribu_atacante]
            codigo = list(a[server].keys())[1]
            lista_atacados_steam_id = a[server][codigo]

            x = get_attacked_users(lista_atacados_steam_id, get_json())

            if x:
                for i in x:

                    fmt = attack_message[read_arg(i, 'lan')]
                    await self.bot.send_message(message.server.get_member_named(i),
                    fmt.format(server, atacador, tribu_atacante, strftime('%I:%M%p %z on %b %d, %Y')))

    async def steam_message(self, user, lan):
        embed = Embed(title=welcome[lan], color=0x4FBCF3)
        embed.add_field(name="Steam ID", value=pre_msg[lan], inline=False)
        embed.set_footer(text=gdrp_msg[lan])
        gdrp = Embed(title=n_help[lan], inline=False)
        gdrp.add_field(name="...", value=_helpo[lan], inline=False)
        gdrp.set_footer(text=gdrp_footer[lan])
        steam_command = Embed(title=how_to_steam[1], color=0x4FBCF3)
        steam_command.add_field(name="...", value=command_exp[lan])
        to_send = [embed, gif[lan], steam_command, command_ss[1], gdrp]
        for i in to_send:
            if isinstance(i, str):
                await self.bot.send_message(user, i)
            else: await self.bot.send_message(user, embed=i)

    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel != self.bot.get_channel("461112442185973760"):
            return

        if reaction.emoji == "🇪🇸":
            await self.steam_message(user, 1)
            update_db({"steam_id": "", "lan": "ES", "ok": False}, user.name)
        elif reaction.emoji == "🇬🇧":
            await self.steam_message(user, 2)
            update_db({"steam_id": "", "lan": "EN", "ok": False}, user.name)
        elif reaction.emoji == "👍":
            try:
                if read_arg(user.name, "ok"):
                    new = find(lambda r: r.name.lower() == 'new', user.server.roles)
                    lan_role = find(lambda r: r.name == read_arg(user.name, "lan"), user.server.roles)
                    await self.bot.remove_roles(user, new)
                    await sleep(5)
                    await self.bot.add_roles(user, lan_role)
            except KeyError:
                x = await self.bot.get_message(self.bot.get_channel("461112442185973760"), "461136423345586186")
                await self.bot.remove_reaction(x, "👍", user)

    async def on_member_join(self, member: discord.Member):
        role = find(lambda r: r.name.lower() == 'kdeservers', member.server.roles)
        if role:
            await self.bot.add_roles(member, role)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
    bot.add_cog(OnMessage(bot))
