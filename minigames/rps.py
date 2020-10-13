import datetime
from random import randint
import discord
from discord.ext import commands
from settings import embedcolor, footer, minigame_channels


class RockPaperScissors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sps", "steen-papier-schaar", "rock-paper-scissors"])
    async def rps(self, ctx, *, question=None):
        if str(ctx.channel) in minigame_channels:
            if question is None:
                await ctx.send(
                    "Dit is geen geldig argument. Probeer opnieuw. "
                    "(Je kan kiezen uit: steen, papier, schaar) [`!rps schaar`]"
                )
            else:
                t = ["papier", "steen", "schaar"]
                responses = t[randint(0, 2)]

                won_embed = discord.Embed(
                    title="Je hebt gewonnen!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Je Wint!**",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                won_embed.set_thumbnail(url=self.client.user.avatar_url)
                won_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                won_embed.set_footer(text=footer)

                lose_embed = discord.Embed(
                    title="Je hebt verloren!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Je Verliest!**",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                lose_embed.set_thumbnail(url=self.client.user.avatar_url)
                lose_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                lose_embed.set_footer(text=footer)

                tie_embed = discord.Embed(
                    title="Je hebt gelijkgespeeld!",
                    description=f"Je koos: **{question}**\nDe bot koos: **{responses}**\n\nUitkomst: **Gelijkspel!**",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                tie_embed.set_thumbnail(url=self.client.user.avatar_url)
                tie_embed.set_author(name="Steen Papier Schaar", icon_url=self.client.user.avatar_url)
                tie_embed.set_footer(text=footer)

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
