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


class setupcmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setup(self, ctx):
        for role in ctx.guild.roles:
            if role.name == '💎│Eigenaar':
                db_maxerg.commit()
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
                embed_color_tuple = maxergdb_cursor.fetchone()
                embed_color = int(embed_color_tuple[0], 16)

                maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
                embed_footer = maxergdb_cursor.fetchone()

                await ctx.channel.purge(limit=2)

                em = discord.Embed(
                    title=f"🎫 Tickets",
                    description=f"Om een ticket aan te maken, reageer met ✅",
                    color=embed_color
                )
                em.set_footer(text=embed_footer[0])
                embed = await ctx.send(embed=em)

                await embed.add_reaction(emoji='✅')

                ticketconfig_sql_messageid = f"UPDATE maxerg_ticket_config SET ticket_message_id = {embed.id}"
                maxergdb_cursor.execute(ticketconfig_sql_messageid)
                db_maxerg.commit()

                ticketconfig_sql_channelid = f"UPDATE maxerg_ticket_config SET ticket_channel_id = {embed.channel.id}"
                maxergdb_cursor.execute(ticketconfig_sql_channelid)
                db_maxerg.commit()


def setup(client):
    client.add_cog(setupcmd(client))
