import discord
from discord.ext import commands
from settings import host, user, password, database, footer, currency, ecogame_channels, embedcolor
import random
from random import randint
import time
import datetime
import mysql.connector


class EcoCrime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 172800, commands.BucketType.user)
    async def crime(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()
            
            failrate = randint(1, 10)

            if failrate == 2 or failrate == 8 or failrate == 10:
                loon = randint(400, 1250)

                maxergdb_cursor.execute(f"SELECT risico FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                risico = maxergdb_cursor.fetchone()

                verlies_job = randint(1, 100)
                if verlies_job <= risico[0]:
                    maxergdb_cursor.execute("UPDATE maxerg_economie SET last_work = %s WHERE user_id = %s", (datetime.datetime.utcnow(), ctx.author.id))
                    maxergdb_cursor.execute("UPDATE maxerg_economie SET job = %s WHERE user_id = %s", ("werkloos", ctx.author.id))
                    maxergdb_cursor.execute("UPDATE maxerg_economie SET risico = %s WHERE user_id = %s", (104, ctx.author.id))

                    em = discord.Embed(
                        title="Job Verloren!",
                        description=f"Je baas is erachter gekomen dat je een crimineel bent. Je bent ontslagen!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
                else:
                    extra_risico = randint(1, 5)
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET risico = risico + {extra_risico} WHERE user_id = {ctx.author.id}")

                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {loon} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto - {loon} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                mogelijke_antwoorden = [f"Je wou een bank beroven maar een hond heeft je aangevallen en je werd opgepakt door de politie en je verloor {currency}{loon}."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0xFF0000
            else:
                loon = randint(850, 3500)
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {loon} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto + {loon} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                mogelijke_antwoorden = [f"Je hebt het huis van een oude vrouw beroofd, je gestolen buit is {currency}{loon}."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0x1bd115

            em = discord.Embed(
                description=f"{antwoord}",
                color=color_succes_fail,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)
            db_maxerg.close()

    @crime.error
    async def crime_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 86400:
                conversion = time.strftime("%#dd %#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            elif 3600 <= cooldown_limit < 86400:
                conversion = time.strftime("%#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            else:
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
    client.add_cog(EcoCrime(client))
