from discord.ext import commands


class Core(commands.Cog):
    @commands.command(name='ping')
    async def ping_cmd(self, ctx):
        await ctx.send('Pong!')

class AdminCore(commands.Cog):
    @commands.command(name='exit')
    async def exit_cmd(self, ctx):
        await ctx.send('Exiting.')
        await ctx.bot.close()

def setup(bot):
    bot.add_cog(Core())
    bot.add_cog(AdminCore())
