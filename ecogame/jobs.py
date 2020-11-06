import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels


class EcoJobs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def jobs(self, ctx, pagina=1):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT prestige FROM maxerg_economie WHERE user_id = {ctx.author.id}")
            prestige = maxergdb_cursor.fetchone()
            prestige = prestige[0]
            db_maxerg.close()

            locked = "<:niet_beschikbaar:759837298912526346>"
            unlocked = "<:beschikbaar:759837298929303603>"

            prestige_one = prestige_two = prestige_three = prestige_four = prestige_five = prestige_six = prestige_seven = prestige_eight = prestige_nine = prestige_ten = prestige_eleven = prestige_twelve = locked

            if prestige >= 1:
                prestige_one = unlocked
            if prestige >= 2:
                prestige_two = unlocked
            if prestige >= 3:
                prestige_three = unlocked
            if prestige >= 4:
                prestige_four = unlocked
            if prestige >= 5:
                prestige_five = unlocked
            if prestige >= 6:
                prestige_six = unlocked
            if prestige >= 7:
                prestige_seven = unlocked
            if prestige >= 8:
                prestige_eight = unlocked
            if prestige >= 9:
                prestige_nine = unlocked
            if prestige >= 10:
                prestige_ten = unlocked
            if prestige >= 11:
                prestige_eleven = unlocked
            if prestige >= 12:
                prestige_twelve = unlocked

            if pagina == 1:
                embed = discord.Embed(
                    description="Jobs met <:niet_beschikbaar:759837298912526346> zijn vergrendeld.\nOm een job te selecteren doe `!job <naam_job>`.",
                    color=embedcolor
                )
                embed.add_field(name="Beschikbare Jobs", value=f"{unlocked} **McDonalds Werker**\nVereiste Prestige: `0` — Loon: `{currency}50 per uur`\n\n"
                                                               f"{prestige_one} **Leerkracht**\nVereiste Prestige: `1` — Loon: `{currency}80 per uur`\n\n"
                                                               f"{prestige_two} **Bouwvakker**\nVereiste Prestige: `2` — Loon: `{currency}120 per uur`\n\n"
                                                               f"{prestige_three} **Politie Agent**\nVereiste Prestige: `3` — Loon: `{currency}180 per uur`\n\n"
                                                               f"{prestige_four} **Boekhouder**\nVereiste Prestige: `4` — Loon: `{currency}240 per uur`\n\n", inline=False)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"{footer} | Pagina {pagina}/3")
                await ctx.send(embed=embed)
            elif pagina == 2:
                embed = discord.Embed(
                    description="Jobs met <:niet_beschikbaar:759837298912526346> zijn vergrendeld.\nOm een job te selecteren doe `!job <naam_job>`.",
                    color=embedcolor
                )
                embed.add_field(name="Beschikbare Jobs", value=f"{prestige_five} **Developer**\nVereiste Prestige: `5` — Loon: `{currency}320 per uur`\n\n"
                                                               f"{prestige_six} **YouTuber**\nVereiste Prestige: `6` — Loon: `{currency}390 per uur`\n\n"
                                                               f"{prestige_seven} **Dokter**\nVereiste Prestige: `7` — Loon: `{currency}450 per uur`\n\n"
                                                               f"{prestige_eight} **Advocaat**\nVereiste Prestige: `8` — Loon: `{currency}520 per uur`\n\n"
                                                               f"{prestige_nine} **Rechter**\nVereiste Prestige: `9` — Loon: `{currency}600 per uur`\n\n", inline=False)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"{footer} | Pagina {pagina}/3")
                await ctx.send(embed=embed)
            elif pagina == 3:
                embed = discord.Embed(
                    description="Jobs met <:niet_beschikbaar:759837298912526346> zijn vergrendeld.\nOm een job te selecteren doe `!job <naam_job>`.",
                    color=embedcolor
                )
                embed.add_field(name="Beschikbare Jobs", value=f"{prestige_ten} **CEO**\nVereiste Prestige: `10` — Loon: `{currency}680 per uur`\n\n"
                                                               f"{prestige_eleven} **Minister**\nVereiste Prestige: `11` — Loon: `{currency}760 per uur`\n\n"
                                                               f"{prestige_twelve} **President**\nVereiste Prestige: `12` — Loon: `{currency}850 per uur`\n\n", inline=False)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"{footer} | Pagina {pagina}/3")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Pagina {pagina} is niet geldig. Geldige pagina's: `1` of `2`.")
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoJobs(client))
