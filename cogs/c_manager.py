from asyncio import sleep

from discord.ext import commands

from Bot.KDE.cogs_manager import load_cogs, unload_cogs


class CogManager:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self):
        unload_cogs(self.bot)
        await self.bot.say('Cogs unloaded')
        await sleep(1)
        load_cogs(self.bot)
        await self.bot.say('Cogs reloaded')


def setup(bot):
    bot.add_cog(CogManager(bot))

