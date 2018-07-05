import discord
from discord.ext import commands
from discord import Embed
from discord.utils import find

from asyncio import sleep
from sys import exit
from json import dump

from Bot.KDE.ark_server_requests import main, cant_jugadores
from Bot.KDE.constants import steam_wrong_msg, okey_message, kde_servers
from Bot.KDE.json_commands import update_db, read_arg, mod_update, read_all, get_json
from Bot.KDE.steam_request import steam_64id, id_parser


def is_mod(ctx):

    role_list = [x.name.lower() for x in ctx.message.author.roles]
    hard_coded_roles = ["moderador esp", "moderador eng", "serveradmin"]
    if hard_coded_roles[0] or hard_coded_roles[1] or hard_coded_roles[2] in role_list:
        return True
    return False


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_mod)
    @commands.command(name="ban", pass_context=True)
    async def ban_user(self, ctx, user: discord.Member, days: int=None, *, reason=None):
        await self.bot.ban(user, delete_message_days=days)
        if reason:
            await self.bot.say(f'User {user} was banned by {ctx.message.author} because of reason/s: {reason}')

    @commands.check(is_mod)
    @commands.command(name='del', pass_context=True)
    async def delete_messages(self, ctx, number: int):

            print(f'{ctx.message.author} deleted {number} messages in {ctx.message.channel}')
            mgs = []
            number = int(number)
            async for x in self.bot.logs_from(ctx.message.channel, limit=number + 1):
                mgs.append(x)
            await self.bot.delete_messages(mgs)

    @commands.check(is_mod)
    @commands.command()
    async def json(self, user: discord.Member):

        await self.bot.say(read_all(user.name))

    @commands.check(is_mod)
    @commands.command(name='jsonupdate')
    async def json_update(self, user: discord.Member, to_update, new_info):
        if to_update not in ['steam_id', 'ok', 'lan']:
            await self.bot.say('Escribelo bien')
            return
        mod_update(user.name, to_update, new_info)

    @commands.check(is_mod)
    @commands.command()
    async def mod(self):

        embed = Embed(title="Comandos de admin", color=0x4FBCF3)
        embed.add_field(name="!ban <@user> <dias>", value="<dias> 1-7, desde donde se les borran los mensajes, "
                                                        "el baneo de momento es permanente", inline=False)
        embed.add_field(name="!del <numero>", value="Borra un <numero> de mensajes del canal donde se use el comando ")
        embed.add_field(name="!json <@usuario>", value="Te dice la informacion de <usuario> en formato json")
        embed.add_field(name="jsonupdate <@usuario> <tag> <nueva_info>", value=""
        "Sirve para actualizar la información"
        "que tenemos de los usuarios a la fuerza"
        "\n tags:"
        "\n <lan> -> lenguaje"
        "\n <steam_id> -> la steam id"
        "\n <ok> -> Toma valor True cuando el usuario ha terminado con exito el registro, cambiarlo sin consultar"
                                                                               " a surister puede dar problemas")
        embed.add_field(name="!getjson", value="Te da la db json entera")
        embed.add_field(name="!load <extension>", value="Sirve para cargar extensiones nuevas al bot")
        embed.add_field(name="!unload <extension>", value="Sirve para descargar extensiones ya cargadas al bot, se "
                                                    "usar de manera maliciosa para cortar el funcionamiento del bot"
                                                    " ,cuidado.")
        embed.add_field(name="!exit", value="Apaga el Bot")
        await self.bot.say(embed=embed)

    @commands.check(is_mod)
    @commands.command(pass_context=True)
    async def rolerino(self, ctx):
        new = find(lambda r: r.name.lower() == 'new', ctx.message.server.roles)
        for i in ctx.message.server.members:
            sleep(2)
            print(i)
            await self.bot.add_roles(i, new)

    @commands.check(is_mod)
    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx, *, user: discord.Member = None):
        x = get_json()
        if user.name in list(x.keys()):
            steamid = read_arg(user.name, "steam_id")
        else:
            steamid = 'No se puede encontrar steam id'

        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = user.joined_at
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.add_field(name="Steam_Id", value=steamid, inline=False)
        data.set_footer(text="Member #{} | User ID:{}"
                             "" .format(member_number, user.id))

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.check(is_mod)
    @commands.command(pass_context=True)
    async def getjson(self, ctx):
        with open('database.json', 'r') as db:
            await self.bot.send_file(ctx.message.channel, db)
            db.close()

    @commands.check(is_mod)
    @commands.command(name='deljson')
    async def del_user_json(self, user: discord.Member):
        a = get_json()
        a.pop(user.name)
        with open('database.json', 'w') as db:
            dump(a, db)
        await self.bot.say(f'He borrado a {user.name} de la base de datos')

    @commands.check(is_mod)
    @commands.command()
    async def msg(self, channel: discord.Channel, *, message):
        await self.bot.send_message(channel, message)

    @commands.command()
    async def server(self, num: int = None):
        if num:
            for w in main(kde_servers[num]):
                await self.bot.say(w)
        else:
            x = cant_jugadores()
            await self.bot.say("Hay {} jugadores conectados en KDE Servers".format(x))


class Loader:
    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_mod)
    @commands.command()
    async def load(self, ext):
        self.bot.load_extension(ext)

        await self.bot.say("Loaded extension {}".format(ext))

    @commands.check(is_mod)
    @commands.command()
    async def unload(self, ext):
        self.bot.unload_extension(ext)
        await self.bot.say("Unloaded extension {}".format(ext))

    @commands.check(is_mod)
    @commands.command(aliases=["exit", "cerrar"])
    async def exi(self):
        exit()


class Login:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["ayuda", "help"])
    async def help_(self, ctx, *, msg=None):
        if isinstance(ctx.message.channel, discord.channel.PrivateChannel):
            try:
                if read_arg(ctx.message.author.name, "ok"):
                    return
            except KeyError:
                return
            fmt = f' comando usado >> {ctx.invoked_with} @everyone El usuario ' \
                  f'{ctx.message.author.mention} ha pedido ayuda  y ha dicho >> {msg}'
            await self.bot.send_message(self.bot.get_channel("456407592621834251"), fmt)

    @commands.command(pass_context=True)
    async def steam(self, ctx, steam):

        if isinstance(ctx.message.channel, discord.channel.PrivateChannel):
            try:
                if read_arg(ctx.message.author.name, "ok"):
                    return
            except KeyError:
                return
            x = steam_64id(id_parser(steam))
            if x:
                update_db(author=ctx.message.author.name, steam=x)
                await self.bot.say(okey_message[read_arg(ctx.message.author.name, "lan")])
                mod_update(ctx.message.author.name, "ok", True)
            else:
                await self.bot.say(steam_wrong_msg[read_arg(ctx.message.author.name, "lan")])


def setup(bot):
    bot.add_cog(Login(bot))
    bot.add_cog(Mod(bot))
    bot.add_cog(Loader(bot))
