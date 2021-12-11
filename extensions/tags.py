from difflib import SequenceMatcher

from discord.ext import commands as cmds
import discord


# Helper for matching search terms with tag names
def match(a, b):
    l, s = (a, b) if len(a) > len(b) else (b, a)
    sm = SequenceMatcher(lambda s: s == ' ', s, l)
    return s in l or round(sm.ratio(), 2) * 100 > 70


class Tag:
    def __init__(self, guild, author, name, content, uses, created, last_used):
        self.guild = guild
        self.author = author
        self.name = name
        self.content = content
        self.uses = uses
        self.created = created
        self.last_used = last_used

    @classmethod
    async def convert(cls, ctx, argument):
        r = await ctx.bot.db.get_tag(argument, ctx.guild.id)
        return cls(r['guild'], r['author'], r['name'], r['content'], r['uses'],
            r['created'], r['last_used'])


class Tags(cmds.Cog):
    @cmds.group(name='tag', aliases=['t', 'tags'], invoke_without_command=True)
    async def tag_cmd(self, ctx, *, tag: Tag):
        target = ctx.message.reference.resolved if ctx.message.reference else ctx
        await target.reply(tag.content)

    @tag_cmd.command(name='new')
    async def tag_new_cmd(self, ctx, name, *, content):
        await ctx.bot.db.new_tag(ctx.guild.id, ctx.author.id, name, content)
        await ctx.reply(f'Tag `{name}` has been created.')

    @tag_cmd.command(name='del')
    async def tag_del_cmd(self, ctx, *, tag: Tag):
        if (ctx.author.id == tag.author or ctx.author.guild_permissions.manage_guild):
            await ctx.bot.db.del_tag(ctx.guild.id, tag.name)
            await ctx.reply(f'Tag `{tag.name}` deleted successfully.')
        else:
            await ctx.reply(f'You do not have permission to delete tag `{tag.name}`')

    # Leaving for now as unsure how to implement.
    @tag_cmd.command(name='alias')
    async def tag_alias_cmd(self, ctx, alias, *, parent):
        pass

    @tag_cmd.command(name='info')
    async def tag_info_cmd(self, ctx, *, tag: Tag):
        author = ctx.guild.get_member(tag.author).name
        created = tag.created.strftime('%d/%m/%y')
        await ctx.reply(f'''Author: {author}\nCreated: {created}''')

    @tag_cmd.command(name='edit')
    async def tag_edit_cmd(self, ctx, tag: Tag, *, content):
        if ctx.author.id == tag.author:
            await ctx.bot.db.edit_tag(ctx.guild.id, tag.name, content)
            await ctx.reply(f'Tag `{tag.name}` has been updated.')
        else:
            await ctx.reply(f'You do not have permission to edit tag `{tag.name}`')

    @tag_cmd.command(name='search')
    async def tag_search_cmd(self, ctx, *, term):
        tags = [_['name'] for _ in await ctx.bot.db.get_tags(ctx.guild.id)]
        matches = filter(lambda x: match(x.lower(), term.lower()), tags)
        await ctx.reply('\n'.join(matches))

    @tag_cmd.command(name='list')
    async def tag_list_cmd(self, ctx, member:discord.Member=None, page=1):
        member = member.id if member else None
        tags = await ctx.bot.db.get_tags(ctx.guild.id, member)
        await ctx.reply('\n'.join([tag['name'] for tag in tags]))

def setup(bot):
    bot.add_cog(Tags())
