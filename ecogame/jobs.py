import datetime
import time
import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels


class EcoJobs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def jobs(self, ctx, pagina=1):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT prestige FROM maxerg_economie WHERE user_id = {ctx.author.id}")
            prestige = maxergdb_cursor.fetchone()
            prestige = prestige[0]

            print(prestige)

            db_maxerg.close()

            locked = "<:niet_beschikbaar:759837298912526346>"
            unlocked = "<:beschikbaar:759837298929303603>"

            prestige_one = locked
            prestige_two = locked
            prestige_three = locked
            prestige_four = locked
            prestige_five = locked
            prestige_six = locked
            prestige_seven = locked
            prestige_eight = locked

            if prestige == 1:
                prestige_one = unlocked
            elif prestige == 2:
                prestige_one = unlocked
                prestige_two = unlocked
            elif prestige == 3:
                prestige_one = unlocked
                prestige_two = unlocked
                prestige_three = unlocked
            elif prestige == 4:
                prestige_one = unlocked
                prestige_two = unlocked
                prestige_three = unlocked
                prestige_four = unlocked
            elif prestige == 5:
                prestige_one = unlocked
                prestige_two = unlocked
                prestige_three = unlocked
                prestige_four = unlocked
                prestige_five = unlocked
            elif prestige == 6:
                prestige_one = unlocked
                prestige_two = unlocked
                prestige_three = unlocked
                prestige_four = unlocked
                prestige_five = unlocked
                prestige_six = unlocked
            elif prestige == 7:
                prestige_one = unlocked
                prestige_two = unlocked
                prestige_three = unlocked
                prestige_four = unlocked
                prestige_five = unlocked
                prestige_six = unlocked
                prestige_seven = unlocked
            elif prestige == 8:
                prestige_one = unlocked
                prestige_two = unlocked
                prestige_three = unlocked
                prestige_four = unlocked
                prestige_five = unlocked
                prestige_six = unlocked
                prestige_seven = unlocked
                prestige_eight = unlocked

            if pagina == 1:
                embed = discord.Embed(
                    description="Jobs met <:niet_beschikbaar:759837298912526346> zijn vergrendeld.\nOm een job te selecteren doe `!job <naam_job>`.",
                    color=embedcolor
                )
                embed.add_field(name="Beschikbare Jobs", value=f"{unlocked} **McDonalds Werker**\nVerplichte Werkuren per dag: `0` — Loon: `{currency}80 per uur`\nVereiste Prestige: `0`\n\n"
                                                               f"{unlocked} **Leerkracht**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}120 per uur`\nVereiste Prestige: `0`\n\n"
                                                               f"{prestige_one} **Bouwvakker**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}150 per uur`\nVereiste Prestige: `1`\n\n"
                                                               f"{prestige_two} **Politie Agent**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}190 per uur`\nVereiste Prestige: `2`\n\n"
                                                               f"{prestige_three} **Developer**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}240 per uur`\nVereiste Prestige: `3`\n\n", inline=False)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"{footer} | Pagina {pagina}/2")
                await ctx.send(embed=embed)
            elif pagina == 2:
                embed = discord.Embed(
                    description="Jobs met <:niet_beschikbaar:759837298912526346> zijn vergrendeld.\nOm een job te selecteren doe `!job <naam_job>`.",
                    color=embedcolor
                )
                embed.add_field(name="Beschikbare Jobs", value=f"{prestige_four} **YouTuber**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}280 per uur`\nVereiste Prestige: `4`\n\n"
                                                               f"{prestige_five} **Dokter**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}330 per uur`\nVereiste Prestige: `5`\n\n"
                                                               f"{prestige_six} **Advocaat**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}390 per uur`\nVereiste Prestige: `6`\n\n"
                                                               f"{prestige_seven} **Rechter**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}440 per uur`\nVereiste Prestige: `7`\n\n"
                                                               f"{prestige_eight} **President**\nVerplichte Werkuren per dag: `1` — Loon: `{currency}500 per uur`\nVereiste Prestige: `8`\n\n", inline=False)
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"{footer} | Pagina {pagina}/2")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Pagina {pagina} is niet geldig. Geldige pagina's: `1` of `2`.")

        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @jobs.error
    async def jobs_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {round(error.retry_after, 1)} seconden wachten om deze command opnieuw te gebruiken.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoJobs(client))
