import discord
from discord.ext import commands
import json
import random
from random import randint
import time
import datetime
import mysql.connector

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']
currency = settings['currency']
embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()

embed_color = int(embedcolor, 16)


class EcoSlut(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def slut(self, ctx):
        minigame_channels = ["💰│economy-game", "🔒│bots"]
        if str(ctx.channel) in minigame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            failrate = randint(0, 3)
            if failrate == 1:
                loon = randint(20, 50)
                loon_cast = int(loon)

                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash - {loon_cast} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto - {loon_cast} WHERE user_id = {ctx.author.id}")
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

                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash + {loon_cast} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto + {loon_cast} WHERE user_id = {ctx.author.id}")
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
            em.set_footer(text=embed_footer)
            await ctx.send(embed=em)

            db_maxerg.close()

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
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer)
            await ctx.send(embed=em)
        else:
            raise error


def setup(client):
    client.add_cog(EcoSlut(client))
