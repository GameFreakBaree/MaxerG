import discord
from discord.ext import commands
import datetime
import json
import asyncio
from random import randint
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()


class Coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
        command_channels = ["🎨│minigames", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            t = ["kop", "munt"]
            responses = t[randint(0, 1)]

            if responses == "kop":
                euro = "https://i.imgur.com/0xVs8Bx.png"
            else:
                euro = "https://i.imgur.com/fco5xCF.png"

            embed = discord.Embed(
                title="Coinflip",
                description=f"Ik heb een muntstuk gegooid en het muntstuk is gevallen op {responses}!",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=f"{euro}")
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)
            db_maxerg.close()
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#721013671307772587> zitten om deze command uit te voeren.")
            await asyncio.sleep(3)
            await del_msg.delete()


def setup(client):
    client.add_cog(Coinflip(client))
