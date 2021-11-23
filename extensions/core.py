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
        await ctx.bot.exit()

class ServerAdminCore(commands.Cog):
    def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        return await super().cog_command_error(ctx, error)

    @commands.group(name='prefix', invoke_without_command=True)
    async def prefix_cmd(self, ctx):
        prefix = await ctx.bot.get_prefix(ctx.message)
        fltr = filter(lambda p: str(ctx.bot.user.id) not in p, prefix)
        await ctx.send(list(fltr))

    @prefix_cmd.command(name='new')
    async def prefix_new_cmd(self, ctx, *, prefix):
        config = ctx.bot.db.get_config(ctx.guild.id)
        config['prefixes'].append(prefix)
        config['in-sync'] = False
        await ctx.reply('New prefix added.')

    @prefix_cmd.command(name='del')
    async def prefix_del_cmd(self, ctx, *, prefix):
        config = ctx.bot.db.get_config(ctx.guild.id, gen=False)

        if config:
            config['prefixes'].remove(prefix)
            config['in-sync'] = False
            await ctx.reply('Prefix removed.')

def setup(bot):
    bot.add_cog(Core())
    bot.add_cog(AdminCore())
    bot.add_cog(ServerAdminCore())
