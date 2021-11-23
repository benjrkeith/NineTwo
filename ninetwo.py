from discord.ext import commands

extensions = ('core',)

def callable_prefix(bot, msg):
    config = bot.db.cache.get(msg.guild.id)
    extras = config['prefixes'] if config else []
    return commands.when_mentioned_or(*extras)(bot, msg)

class NineTwo(commands.AutoShardedBot):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        super().__init__(callable_prefix, *args, **kwargs)

        for ext in extensions:
            self.load_extension(f'extensions.{ext}')
