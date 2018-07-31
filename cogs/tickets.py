from discord.ext import commands
from discord import Embed
from time import strftime

from Bot.KDE.extras import ticket_num_generator
from Bot.KDE.json_commands import read_arg
from Bot.KDE.constants import ticket_memo


class Tickets:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def nomore(self, ctx, _type: int, *, msg):
        users_language = read_arg(ctx.message.author.name, 'lan')
        x = ticket_num_generator(users_language)
        embed = Embed(title=f'Ticket Nº {x}')
        embed.set_footer(text=strftime('%I:%M%p %z on %b %d %Y'))
        embed.set_author(name=f'{ctx.message.author.name} / {read_arg(ctx.message.author.name, "steam_id")}')
        embed.add_field(name=ticket_memo[users_language][_type], value=msg)
        await self.bot.say(embed=embed)

    @commands.command(name="open")
    async def open_ticket(self):
        pass


def setup(bot):
    bot.add_cog(Tickets(bot))
