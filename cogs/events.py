from asyncio import sleep
from time import time


from discord import Member, Embed, Game
from discord.ext import commands
from discord.utils import find

from Bot.KDE.constants import *
from Bot.KDE.constants import __version__
from Bot.KDE.constants import _helpo
from Bot.KDE.extras import get_attacked_users, players_wh, switcher_wh, info_switcher_wh, server_wh
from Bot.KDE.json_commands import update_db, read_arg, str_to_dic, get_json


class OnReady:

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        await self.bot.change_presence(game=Game(name="Ark Survival Evolved"))
        before = time()

        a = self.bot.get_channel('461112442185973760')
        b = await self.bot.get_message(a, '461136423345586186')
        self.bot.messages.append(b)

        after = time()
        s = '\n----------------------------\n'
        fmt = "--v:" + __version__ + "\nConectado como: {0} \n Id: {1} \n It took to init the bot {2}".format(
            self.bot.user.name,
            self.bot.user.id,
            after - before)
        print(s, fmt, s)


class CommandErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.CommandNotFound):
            await self.bot.send_message(ctx.message.channel, "That command does not exist")
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.bot.send_message(ctx.message.channel, "Missing required argument")
        elif isinstance(error, ValueError):
            await self.bot.send_message(ctx.message.channel, "!info @user")
        else:
            await self.bot.send_message(ctx.message.channel, error)
            # print(strftime('%c'), " ", error)

    @staticmethod
    async def on_error(event):
        print(event)


class OnMessageVariable:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.channel == self.bot.get_channel("462267741152346112"):

            b = str_to_dic(message.content)
            final_switcher = switcher_wh(b)
            server = server_wh(b)
            time = strftime('%I:%M%p %z on %b %d %Y')

            if final_switcher == '1':
                fmt = (server, info_switcher_wh(b)[1], info_switcher_wh(b)[0], time)
            if final_switcher == '2':
                fmt = (server, info_switcher_wh(b)[0], time)
            if final_switcher == '3':
                fmt = (server, info_switcher_wh(b)[1], info_switcher_wh(b)[0], time)
            if final_switcher == '4':
                fmt = (server, info_switcher_wh(b)[0], time)
            if final_switcher == '5':
                fmt = (server, info_switcher_wh(b)[0], time)
            if final_switcher == '6':
                fmt = (server, time)

            for discord_users in get_attacked_users(players_wh(b), get_json()):

                await self.bot.send_message(message.server.get_member_named(discord_users),
                                            wb_msg[read_arg(discord_users, 'lan')][switcher_wh(b)].format(*fmt))

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
            else:
                await self.bot.send_message(user, embed=i)

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
                    if read_arg(user.name, "lan") == 'EN':
                        lan_role = find(lambda r: r.name == 'ENG', user.server.roles)
                    else:
                        lan_role = find(lambda r: r.name == 'ES', user.server.roles)
                    await self.bot.remove_roles(user, new)
                    await sleep(5)
                    await self.bot.add_roles(user, lan_role)
            except KeyError:
                x = await self.bot.get_message(self.bot.get_channel("461112442185973760"), "461136423345586186")
                await self.bot.remove_reaction(x, "👍", user)

    async def on_member_join(self, member: Member):
        role = find(lambda r: r.name.lower() == 'new', member.server.roles)
        if role:
            await self.bot.add_roles(member, role)

    @staticmethod
    async def on_resumed():
        print("bots going down")


def setup(bot):
    bot.add_cog(OnMessageVariable(bot))
    bot.add_cog(CommandErrorHandler(bot))
    bot.add_cog(OnReady(bot))
