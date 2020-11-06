from discord.ext import commands
import mysql.connector
from settings import host, user, password, database


class OnLeave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stats_channel = self.client.get_channel(640341412306485251)
        guild_ids = stats_channel.guild

        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        maxergdb_cursor.execute(f"DELETE FROM maxerg_economie WHERE user_id = {member.id}")
        maxergdb_cursor.execute(f"DELETE FROM maxerg_levels WHERE user_id = {member.id}")
        db_maxerg.commit()
        db_maxerg.close()

        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnLeave(client))
