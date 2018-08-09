from discord.ext import commands
from discord import Embed
from Bot.KDE.json_commands import read_db

from Bot.KDE.constants import *


class Test:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def alr(self):
        await self.bot.say("ws")

    @commands.command()
    async def okays(self, lan: int):
        embed = Embed(title=disc_message_0[lan], description=disc_message_1[lan], color=0xf34fe9)
        embed.add_field(name='\u200b\u200b\u200b\u200b\u200b', value='\u200b')
        embed.add_field(name='\u200b', value=discord_message_2[lan])
        embed.add_field(name='\u200b\u200b\u200b\u200b\u200b', value='\u200b')
        embed.set_image(url='https://cdn.discordapp.com/attachments/463147317898379284/466976538576027667/sss.gif')

        await self.bot.say(embed=embed)
        await self.bot.say(disc_message_3[lan])


def setup(bot):
    bot.add_cog(Test(bot))
