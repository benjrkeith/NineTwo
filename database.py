import asyncpg

from config import DATABASE


GUILDS_TABLE = '''CREATE TABLE IF NOT EXISTS guilds(id BIGINT PRIMARY KEY,
                    prefixes TEXT[] NOT NULL);'''

TAG_TABLE = '''CREATE TABLE IF NOT EXISTS tags(guild BIGINT NOT NULL,
                author BIGINT NOT NULL, name TEXT NOT NULL, 
                content TEXT NOT NULL, uses INT DEFAULT 0, 
                created TIMESTAMPTZ default current_timestamp(0), 
                last_used TIMESTAMPTZ, PRIMARY KEY(name, guild));'''

TABLES = [GUILDS_TABLE, TAG_TABLE]


class Database:
    def __init__(self):
        self.cache = {}
        self.conn = None

    async def initialise(self):
        self.conn = await asyncpg.connect(**DATABASE)
        for stat in TABLES:
            await self.conn.execute(stat)
        await self.pull_configs()

    async def push_configs(self):
        async with self.conn.transaction():
            for conf in self.cache.values():
                if conf.get('in-sync', True):
                    continue

                if conf.get('in-db', True):
                    stat = 'UPDATE guilds SET prefixes = $2 WHERE id = $1'
                else:
                    stat = 'INSERT INTO guilds VALUES ($1, $2)'

                await self.conn.execute(stat, conf['id'], conf['prefixes'])
                conf['in-sync'] = conf['in-db'] = True

    async def pull_configs(self):
        records = await self.conn.fetch('SELECT * FROM guilds')
        self.cache = {r['id']: {k: v for k, v in r.items()} for r in records}

    def get_config(self, guild_id, gen=True):
        conf = self.cache.get(guild_id)
        return conf if conf else self.new_config(guild_id) if gen else None

    def new_config(self, guild_id):
        self.cache[guild_id] = {'id': guild_id, 'prefixes': [],
                                'in-sync': False, 'in-db': False}
        return self.cache[id]

    async def get_tag(self, tag, guild):
        stat = 'SELECT * FROM tags WHERE name=$1 AND guild=$2'
        return await self.conn.fetchrow(stat, tag, guild)

    async def get_tags(self, guild, member=None):
        if (member):
            stat = 'SELECT name FROM tags WHERE guild=$1 AND author=$2'
            return await self.conn.fetch(stat, guild, member)

        stat = 'SELECT name FROM tags WHERE guild=$1'
        return await self.conn.fetch(stat, guild)

    async def new_tag(self, guild, author, name, content):
        stat = '''INSERT INTO tags(guild, author, name, content)
                    VALUES($1, $2, $3, $4);'''
        await self.conn.execute(stat, guild, author, name, content)

    async def del_tag(self, guild, tag):
        stat = 'DELETE FROM tags WHERE guild=$1 AND name=$2'
        await self.conn.execute(stat, guild, tag)

    async def edit_tag(self, guild, tag, content):
        stat = 'UPDATE tags SET content=$1 WHERE guild=$2 AND name=$3'
        await self.conn.execute(stat, content, guild, tag)

    async def close(self):
        await self.push_configs()
        await self.conn.close()
