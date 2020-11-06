import discord
from discord.ext import commands
from random import randint
import time
import datetime
import mysql.connector
from settings import host, user, password, database, footer, currency, ecogame_channels, prefix, errorcolor


class EcoFish(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 2700, commands.BucketType.user)
    async def fish(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            embedcolor = 0x1bd115
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT vishengel FROM maxerg_inventory WHERE user_id = {ctx.author.id}")
            vishengel = maxergdb_cursor.fetchone()

            if vishengel[0] == 1:
                loon = randint(80, 350)
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {loon}, netto = netto + {loon} WHERE user_id = {ctx.author.id}")
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
                    description=f"Je hebt geen vishengel! Om er 1 te kopen doe `{prefix}shop koop vishengel`.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @fish.error
    async def fish_error(self, ctx, error):
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
    client.add_cog(EcoFish(client))
