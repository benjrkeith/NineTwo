from discord.ext import commands


class Core(commands.Cog):
    @commands.command(name='ping')
    async def ping_cmd(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name='addpre')
    async def db_addpre(self, ctx, *prefixes):
        config = ctx.bot.db.cache.get(ctx.guild.id)
        config['prefixes'].extend(prefixes)
        config['in-sync'] = False
        await ctx.send('Prefixes updated.')

class AdminCore(commands.Cog):
    def cog_check(self, ctx):
        return ctx.author.id == 419599149596672001

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Only my admins can use this command.')

    @commands.command(name='exit')
    async def exit_cmd(self, ctx):
        await ctx.send('Exiting.')
        await ctx.bot.db.close()
        await ctx.bot.close()

def setup(bot):
    bot.add_cog(Core())
    bot.add_cog(AdminCore())
