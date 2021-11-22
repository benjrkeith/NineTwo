from discord.ext import commands


extensions = ('core',)

class NineTwo(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__('>', *args, **kwargs)

        for ext in extensions:
            self.load_extension(f'extensions.{ext}')
