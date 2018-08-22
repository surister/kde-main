import os

from Bot.KDE.paths import cogs_path


class StartupExtension:

    blacklist = ['__pycache__']

    @classmethod
    def to_array(cls):

        return [f'cogs.{cog}'.replace('.py', '') for cog in os.listdir(cogs_path) if cog not in
                                                                                        StartupExtension().blacklist]


startup_list = StartupExtension.to_array()
