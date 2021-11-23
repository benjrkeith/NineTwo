from discord.ext import commands
from config import DEFAULT_PREFIX


extensions = ('core',)

def callable_prefix(bot, msg):
    config = bot.db.cache.get(msg.guild.id)
    return config["prefixes"] if config else DEFAULT_PREFIX

class NineTwo(commands.AutoShardedBot):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        super().__init__(callable_prefix, *args, **kwargs)

        for ext in extensions:
            self.load_extension(f'extensions.{ext}')
