import datetime
import json
from random import randint
import discord
from discord.ext import commands

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
                won_embed.set_footer(text=embed_footer)

                lose_embed = discord.Embed(
                    title="Je hebt verloren!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Je Verliest!**",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                lose_embed.set_thumbnail(url=self.client.user.avatar_url)
                lose_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                lose_embed.set_footer(text=embed_footer)

                tie_embed = discord.Embed(
                    title="Je hebt gelijkgespeeld!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Gelijkspel!**",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                tie_embed.set_thumbnail(url=self.client.user.avatar_url)
                tie_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                tie_embed.set_footer(text=embed_footer)

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


def setup(client):
    client.add_cog(RockPaperScissors(client))
