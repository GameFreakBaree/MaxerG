import discord
from discord.ext import commands
import datetime
from random import randint
from settings import embedcolor, footer, minigame_channels


class Coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
        if str(ctx.channel) in minigame_channels:
            t = ["kop", "munt"]
            responses = t[randint(0, 1)]

            if responses == "kop":
                euro = "https://i.imgur.com/0xVs8Bx.png"
            else:
                euro = "https://i.imgur.com/fco5xCF.png"

            embed = discord.Embed(
                title="Coinflip",
                description=f"Ik heb een muntstuk gegooid en het muntstuk is gevallen op {responses}!",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=f"{euro}")
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Coinflip(client))
