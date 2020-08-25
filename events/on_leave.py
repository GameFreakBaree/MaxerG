from discord.ext import commands
import json
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()

db_maxerg = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    passwd=password
)

maxergdb_cursor = db_maxerg.cursor()

maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
embed_footer = maxergdb_cursor.fetchone()


class OnJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stats_channel = self.client.get_channel(742705535899533333)
        guild_ids = stats_channel.guild

        log_channel = self.client.get_channel(742715965128704030)
        await log_channel.send(f"<:times:742717346472525845> {member} is geleaved!")

        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnJoin(client))
