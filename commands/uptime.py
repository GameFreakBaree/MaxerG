import discord
import datetime
import time
import json
from discord.ext import commands
import mysql.connector

start_time = time.time()

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

maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
embed_color_tuple = maxergdb_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)

maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
embed_footer = maxergdb_cursor.fetchone()


class Uptime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def uptime(self, ctx):
        command_channels = ["🤖│commands", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))

            embed = discord.Embed(
                title="Uptime",
                description=f"{text}",
                color=embed_color
            )
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Uptime(client))
