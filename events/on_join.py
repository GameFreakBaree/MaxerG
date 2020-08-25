import discord
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
    async def on_member_join(self, member):
        join_channel = self.client.get_channel(739810780735602761)
        stats_channel = self.client.get_channel(742705535899533333)
        guild_ids = stats_channel.guild

        embed = discord.Embed(
            description=f"Welkom **{member.display_name}** bij **{guild_ids.name}**!",
            color=0x00FF00
        )
        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.set_footer(
            text=f"{embed_footer[0]} | Speler #{guild_ids.member_count}",
            icon_url=self.client.user.avatar_url
        )
        await join_channel.send(embed=embed)

        log_channel = self.client.get_channel(742715965128704030)
        await log_channel.send(f"<:check:742717346128593099> {member} is gejoined!")

        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnJoin(client))
