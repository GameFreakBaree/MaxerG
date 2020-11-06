import discord
from discord.ext import commands
import time
from random import randint
import datetime
import mysql.connector
from settings import host, user, password, database, footer, currency, ecogame_channels, errorcolor


class EcoWork(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            embedcolor = 0x1bd115
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT job FROM maxerg_economie WHERE user_id = {ctx.author.id}")
            current_job = maxergdb_cursor.fetchone()
            current_job = current_job[0]

            doorgaan = True
            loon = 0

            if current_job == "werkloos":
                doorgaan = False
            elif current_job == "mcdonalds werker":
                loon = 50
            elif current_job == "leerkracht":
                loon = 80
            elif current_job == "bouwvakker":
                loon = 120
            elif current_job == "politie agent":
                loon = 180
            elif current_job == "boekhouder":
                loon = 240
            elif current_job == "developer":
                loon = 320
            elif current_job == "youtuber":
                loon = 390
            elif current_job == "dokter":
                loon = 450
            elif current_job == "advocaat":
                loon = 520
            elif current_job == "rechter":
                loon = 600
            elif current_job == "ceo":
                loon = 680
            elif current_job == "minister":
                loon = 760
            elif current_job == "president":
                loon = 850
            else:
                doorgaan = False

            if doorgaan:
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + %s WHERE user_id = %s", (loon, ctx.author.id))
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto + %s WHERE user_id = %s", (loon, ctx.author.id))
                db_maxerg.commit()

                em = discord.Embed(
                    description=f"{ctx.author.display_name} heeft 1 uur gewerkt en verdiende {currency}{loon}",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=footer)
                await ctx.send(embed=em)
            else:
                await ctx.send("Je hebt geen job. doe `!jobs` om een job te selecteren.")
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            conversion = time.strftime("%-Mm %-Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=errorcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoWork(client))
