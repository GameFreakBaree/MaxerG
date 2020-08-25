import discord
from discord.ext import commands
import json
import random
from random import randint
import time
import datetime
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

maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
embed_color_tuple = maxergdb_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)

maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
embed_footer = maxergdb_cursor.fetchone()

maxergdb_cursor.execute("SELECT currency FROM maxerg_config")
currency_tuple = maxergdb_cursor.fetchone()
currency = currency_tuple[0]


class EcoSlut(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def slut(self, ctx):
        minigame_channels = ["💰│economy-game", "🔒│bots"]
        if str(ctx.channel) in minigame_channels:
            db_maxerg.commit()

            failrate = randint(0, 3)
            if failrate == 1:
                loon = randint(20, 50)
                loon_cast = int(loon)

                maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {ctx.author.id}")
                cash = maxergdb_cursor.fetchone()
                if cash is None:
                    cash = (0,)
                cash_new = cash[0] - loon_cast

                ecogame_sql_cash = f"UPDATE maxerg_ecogame SET cash = {cash_new} WHERE user_id = {ctx.author.id}"
                maxergdb_cursor.execute(ecogame_sql_cash)
                db_maxerg.commit()

                mogelijke_antwoorden = [
                    f"De politie viel je huis binnen en je kreeg een boete van {currency}{loon_cast}.",
                    f"Een klant viel je aan en heeft {currency}{loon_cast} genomen en is weggelopen.",
                    f"Je bent betrapt toen je een leuke tijd had in de badkamer en kreeg een boete van {currency}{loon_cast}.",
                    f"Je vibrator viel in het midden van je show uit, je klant wou een stuk van zijn geld terug, dus je hebt hem {currency}{loon_cast} betaald.",
                    f"Je was naakt aan het wandelen op de straat en kreeg een boete van {currency}{loon_cast} voor het verstoren van de openbare orde."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0xFF0000
            else:
                loon = randint(30, 60)
                loon_cast = int(loon)

                maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {ctx.author.id}")
                cash = maxergdb_cursor.fetchone()
                if cash is None:
                    cash = (0,)
                cash_new = cash[0] + loon_cast

                ecogame_sql_cash = f"UPDATE maxerg_ecogame SET cash = {cash_new} WHERE user_id = {ctx.author.id}"
                maxergdb_cursor.execute(ecogame_sql_cash)
                db_maxerg.commit()

                mogelijke_antwoorden = [f"Je kreeg {currency}{loon_cast} om te dansen in een stripclub.",
                                        f"Je Suger Daddy betaalde je {currency}{loon_cast} voor het werk dat je deed voor hem vorige nacht.",
                                        f"Je bent heel goed met je handen en kreeg {currency}{loon_cast}.",
                                        f"Je hebt {currency}{loon_cast} verdient om naaktfoto's online te verkopen.",
                                        f"Je hebt een Onlyfans gestart en verdiende {currency}{loon_cast} op de eerste dag."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0x1bd115

            em = discord.Embed(
                description=f"{antwoord}",
                color=color_succes_fail,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer[0])
            await ctx.send(embed=em)
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#747575812605214900> zitten om deze command uit te voeren.")
            time.sleep(3)
            await del_msg.delete()

    @slut.error
    async def slut_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 86400:
                conversion = time.strftime("%#dd %#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            elif 3600 <= cooldown_limit < 86400:
                conversion = time.strftime("%#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            else:
                conversion = time.strftime("%#Mm %#Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"X Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer[0])
            await ctx.send(embed=em)
        else:
            raise error


def setup(client):
    client.add_cog(EcoSlut(client))
