from discord.ext import commands as cmds
from discord.ext.commands import errors


class Core(cmds.Cog):
    @cmds.command(name='ping')
    async def ping_cmd(self, ctx):
        await ctx.reply('Pong!')


class AdminCore(cmds.Cog):
    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, errors.CheckFailure):
            await ctx.reply('Only my admins can use this command.')

    @cmds.command(name='exit')
    async def exit_cmd(self, ctx):
        await ctx.reply('Exiting.')
        await ctx.bot.exit()

    @cmds.group(name='ext', invoke_without_command=True)
    async def ext_cmd(self, ctx):
        await ctx.reply('\n'.join(ctx.bot.extensions.keys()))

    @ext_cmd.command(name='load')
    async def ext_load_cmd(self, ctx, ext):
        ext = f'extensions.{ext}'
        try:
            ctx.bot.load_extension(ext)
        except [errors.ExtensionNotFound, errors.ExtensionAlreadyLoaded]:
            await ctx.reply(f'`{ext}` could not be loaded.')
        finally:
            await ctx.reply(f'`{ext}` has been loaded.')

    @ext_cmd.command(name='unload')
    async def ext_unload_cmd(self, ctx, ext):
        if ext == 'core':
            return await ctx.reply(f'`{ext}` is required.')

        ext = f'extensions.{ext}'
        try:
            ctx.bot.unload_extension(ext)
        except [errors.ExtensionNotFound, errors.ExtensionNotLoaded]:
            await ctx.reply('`{ext}` could not be unloaded.')
        finally:
            await ctx.reply(f'`{ext}` has been unloaded.')

    @ext_cmd.command(name='reload')
    async def ext_reload_cmd(self, ctx, ext):
        ext = f'extensions.{ext}'
        try:
            ctx.bot.reload_extension(ext)
        except [errors.ExtensionNotLoaded, errors.ExtensionNotFound]:
            await ctx.reply('`{ext}` could not be reloaded.')
        finally:
            await ctx.reply(f'`{ext}` has been reloaded.')


class ServerAdminCore(cmds.Cog):
    def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_guild

    async def cog_command_error(self, ctx, error):
        if isinstance(error, errors.CheckFailure):
            await ctx.reply('Only server admins can use this command.')

    @cmds.group(name='prefix', invoke_without_command=True)
    async def prefix_cmd(self, ctx):
        prefix = await ctx.bot.get_prefix(ctx.message)
        fltr = filter(lambda p: str(ctx.bot.user.id) not in p, prefix)
        await ctx.reply('\n'.join(list(fltr)))

    @prefix_cmd.command(name='new')
    async def prefix_new_cmd(self, ctx, *, prefix):
        config = ctx.bot.db.get_config(ctx.guild.id)
        config['prefixes'].append(prefix)
        config['in-sync'] = False
        await ctx.reply(f'`{prefix}` added to prefixes.')

    @prefix_cmd.command(name='del')
    async def prefix_del_cmd(self, ctx, *, prefix):
        config = ctx.bot.db.get_config(ctx.guild.id, gen=False)

        if config:
            config['prefixes'].remove(prefix)
            config['in-sync'] = False
            await ctx.reply(f'`{prefix}` removed from prefixes.')


def setup(bot):
    bot.add_cog(Core())
    bot.add_cog(AdminCore())
    bot.add_cog(ServerAdminCore())
