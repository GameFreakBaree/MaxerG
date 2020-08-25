import datetime
import json
import time
from random import randint
import discord
from discord.ext import commands
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

maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
embed_color_tuple = maxergdb_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)


class RockPaperScissors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sps", "steen-papier-schaar", "rock-paper-scissors"])
    async def rps(self, ctx, *, question=None):
        if question is None:
            await ctx.send(
                "Dit is geen geldig argument. Probeer opnieuw. "
                "(Je kan kiezen uit: steen, papier, schaar) [`!rps schaar`]"
            )
        else:
            minigame_channels = ["🎨│minigames", "🔒│bots"]
            if str(ctx.channel) in minigame_channels:
                t = ["papier", "steen", "schaar"]
                responses = t[randint(0, 2)]

                won_embed = discord.Embed(
                    title="Je hebt gewonnen!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Je Wint!**",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                won_embed.set_thumbnail(url=self.client.user.avatar_url)
                won_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                won_embed.set_footer(text=embed_footer[0])

                lose_embed = discord.Embed(
                    title="Je hebt verloren!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Je Verliest!**",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                lose_embed.set_thumbnail(url=self.client.user.avatar_url)
                lose_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                lose_embed.set_footer(text=embed_footer[0])

                tie_embed = discord.Embed(
                    title="Je hebt gelijkgespeeld!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Gelijkspel!**",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                tie_embed.set_thumbnail(url=self.client.user.avatar_url)
                tie_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                tie_embed.set_footer(text=embed_footer[0])

                if question == responses:
                    await ctx.send(embed=tie_embed)
                elif question == "steen":
                    if responses == "papier":
                        await ctx.send(embed=lose_embed)
                    else:
                        await ctx.send(embed=won_embed)
                elif question == "papier":
                    if responses == "schaar":
                        await ctx.send(embed=lose_embed)
                    else:
                        await ctx.send(embed=won_embed)
                elif question == "schaar":
                    if responses == "steen":
                        await ctx.send(embed=lose_embed)
                    else:
                        await ctx.send(embed=won_embed)
                else:
                    await ctx.send(
                        "Dit is geen geldig argument. Probeer opnieuw. (Je kan kiezen uit: steen, papier, schaar)")
            else:
                await ctx.channel.purge(limit=1)
                del_msg = await ctx.send(f"Je moet in <#721013671307772587> zitten om deze command uit te voeren.")
                time.sleep(3)
                await del_msg.delete()


def setup(client):
    client.add_cog(RockPaperScissors(client))
