import asyncpg

from config import DATABASE


class Database:
    def __init__(self):
        self.cache = {}
        self.conn = None

    async def initialise(self):
        stat = '''CREATE TABLE IF NOT EXISTS guilds(
            id BIGINT PRIMARY KEY,
            prefixes TEXT[] NOT NULL);'''
        self.conn = await asyncpg.connect(**DATABASE)
        await self.conn.execute(stat)
        await self.pull()

    async def push(self):
        async with self.conn.transaction():
            for conf in self.cache.values():
                if conf.get('in-sync', True):
                    continue

                if conf.get('in-db', True):
                    stat = 'UPDATE guilds SET prefixes = $2 WHERE id = $1'
                else:
                    stat = 'INSERT INTO guilds VALUES ($1, $2)'

                await self.conn.execute(stat, conf['id'], conf['prefixes'])
                conf['in-sync'] = True

    async def pull(self):
        records = await self.conn.fetch('SELECT * FROM guilds')
        self.cache = {r['id']: {k: v for k, v in r.items()} for r in records}

    async def close(self):
        await self.push()
        await self.conn.close()
