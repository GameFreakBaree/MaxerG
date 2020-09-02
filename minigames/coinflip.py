import discord
from discord.ext import commands
import datetime
import json
from random import randint

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']
embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()

embed_color = int(embedcolor, 16)


class Coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
        command_channels = ["🎨│minigames", "🔒│bots"]
        if str(ctx.channel) in command_channels:
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
            embed.set_footer(text=embed_footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Coinflip(client))
