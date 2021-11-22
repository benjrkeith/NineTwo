from discord.ext import commands


class Core(commands.Cog):
    @commands.command(name='ping')
    async def ping_cmd(self, ctx):
        await ctx.send('Pong!')

class AdminCore(commands.Cog):
    def cog_check(self, ctx):
        return ctx.author.id == 419599149596672001

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Only my admins can use this command.')

    @commands.command(name='exit')
    async def exit_cmd(self, ctx):
        await ctx.send('Exiting.')
        await ctx.bot.close()

def setup(bot):
    bot.add_cog(Core())
    bot.add_cog(AdminCore())
