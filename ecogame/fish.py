import discord
from discord.ext import commands
from random import randint
import time
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels, prefix


class EcoFish(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def fish(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT vishengel FROM maxerg_inventory WHERE user_id = {ctx.author.id}")
            vishengel = maxergdb_cursor.fetchone()

            if vishengel[0] == 1:
                loon = randint(25, 400)
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {loon} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto + {loon} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                embed = discord.Embed(
                    description=f"Je hebt een vis gevangen en verkocht hem voor {currency}{loon}.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"Je hebt geen vishengel! Om er 1 te kopen doe `{prefix}shop list`.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            db_maxerg.close()

    @fish.error
    async def fish_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 3600:
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
    client.add_cog(EcoFish(client))
