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


class EcoCrime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def crime(self, ctx):
        minigame_channels = ["💰│economy-game", "🔒│bots"]
        if str(ctx.channel) in minigame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            failrate = randint(0, 3)
            if failrate != 1:
                loon = randint(120, 180)
                loon_cast = int(loon)

                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash - {loon_cast} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto - {loon_cast} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                mogelijke_antwoorden = [
                    f"Je wou een bank beroven maar een hond heeft je aangevallen en je werd opgepakt door de politie en je verloor {currency}{loon_cast}."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0xFF0000
            else:
                loon = randint(250, 500)
                loon_cast = int(loon)

                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash + {loon_cast} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto + {loon_cast} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                mogelijke_antwoorden = [
                    f"Je hebt het huis van een oude vrouw beroofd, je gestolen buit is {currency}{loon_cast}."]
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
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer)
            await ctx.send(embed=em)
        else:
            raise error


def setup(client):
    client.add_cog(EcoCrime(client))
