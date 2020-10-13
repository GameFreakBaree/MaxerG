import discord
from discord.ext import commands
import time
from random import randint
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels


class EcoWork(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
            eco_data = maxergdb_cursor.fetchone()
            current_job = eco_data[5]
            last_work_time = eco_data[6]
            risico = eco_data[7]

            doorgaan = True
            loon = 0

            if current_job == "werkloos":
                doorgaan = False
            elif current_job == "mcdonalds werker":
                loon = 80
            elif current_job == "leerkracht":
                loon = 120
            elif current_job == "bouwvakker":
                loon = 150
            elif current_job == "politie agent":
                loon = 190
            elif current_job == "developer":
                loon = 240
            elif current_job == "youtuber":
                loon = 280
            elif current_job == "dokter":
                loon = 330
            elif current_job == "advocaat":
                loon = 390
            elif current_job == "rechter":
                loon = 440
            elif current_job == "president":
                loon = 500
            else:
                doorgaan = False

            if doorgaan:
                current_time = datetime.datetime.utcnow()
                tijd = current_time - last_work_time
                last_work = current_time.strftime("%Y-%m-%d %H:%M:%S")
                if tijd.total_seconds() > 86400 and current_job != "mcdonalds werker":
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET job = %s WHERE user_id = %s", ("werkloos", ctx.author.id))
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET risico = %s WHERE user_id = %s", (104, ctx.author.id))
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET last_work = %s WHERE user_id = %s", (last_work, ctx.author.id))
                    db_maxerg.commit()

                    em = discord.Embed(
                        description=f"Je hebt niet genoeg gewerkt in de afgelopen 24u! Je bent Ontslagen!\nJe hebt een cooldown van `7 dagen` om terug te solliciteren.",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
                else:
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + %s WHERE user_id = %s", (loon, ctx.author.id))
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto + %s WHERE user_id = %s", (loon, ctx.author.id))
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET last_work = %s WHERE user_id = %s", (last_work, ctx.author.id))
                    if 0 < risico < 100:
                        if risico <= 10:
                            random_procent = 1
                        else:
                            random_procent = randint(1, 3)
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET risico = risico - %s WHERE user_id = %s", (random_procent, ctx.author.id))
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
                ctx.command.reset_cooldown(ctx)
            db_maxerg.close()
        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            conversion = time.strftime("%#Mm %#Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoWork(client))
