from discord.ext import commands as cmds


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
    @cmds.group(name='tag', aliases=['t'], invoke_without_command=True)
    async def tag_cmd(self, ctx, *, tag: Tag):
        await ctx.reply(tag.content)

    @tag_cmd.command(name='new')
    async def tag_new_cmd(self, ctx, name, *, content):
        pass

    @tag_cmd.command(name='del')
    async def tag_del_cmd(self, ctx, *, name):
        pass

    @tag_cmd.command(name='alias')
    async def tag_alias_cmd(self, ctx, alias, *, parent):
        pass

    @tag_cmd.command(name='info')
    async def tag_info_cmd(self, ctx, *, tag: Tag):
        await ctx.reply(f'Author: {ctx.guild.get_member(tag.author).name}')

    @tag_cmd.command(name='edit')
    async def tag_edit_cmd(self, ctx, name, *, content):
        pass

    @tag_cmd.command(name='search')
    async def tag_search_cmd(self, ctx, *, term):
        pass

    @tag_cmd.command(name='list')
    async def tag_list_cmd(self, ctx, page, user):
        pass

def setup(bot):
    bot.add_cog(Tags())