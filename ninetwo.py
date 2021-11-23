from discord.ext import commands
import discord

extensions = ('core', 'tags')

def callable_prefix(bot, msg):
    config = bot.db.cache.get(msg.guild.id)
    extras = config['prefixes'] if config else []
    return commands.when_mentioned_or(*extras)(bot, msg)

class NineTwo(commands.AutoShardedBot):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        intents = discord.Intents.all()
        super().__init__(callable_prefix, intents=intents, *args, **kwargs)

        for ext in extensions:
            self.load_extension(f'extensions.{ext}')

    async def exit(self):
        await self.db.close()
        await self.close()
