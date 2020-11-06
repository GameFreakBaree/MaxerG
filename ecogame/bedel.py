import discord
from discord.ext import commands
import random
from random import randint
import time
import datetime
import mysql.connector
from settings import host, user, password, database, footer, currency, ecogame_channels, errorcolor


class EcoBedel(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def bedel(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT prestige FROM maxerg_economie WHERE user_id = {ctx.author.id}")
            prestige = maxergdb_cursor.fetchone()

            if prestige[0] <= 2:
                mogelijke_namen = ["Jonathan", "Siebe", "Max", "Jeff", "Sebastian",
                                   "Bryan", "Pieter", "Bert", "John", "Ben",
                                   "Willem", "Tibo", "Sem", "Daniel", "Cedric",
                                   "Fleur", "Emma", "Bo", "Amy", "Charlotte",
                                   "Elon", "Mark", "Witse", "Jorrit", "Bram"]
                naam = random.choice(mogelijke_namen)

                loon = randint(45, 120)
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {loon}, netto = netto + {loon} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                antwoord = f"{naam} heeft {currency}{loon} gegeven aan {ctx.author.mention}!"
                color_succes_fail = 0x1bd115

                em = discord.Embed(
                    description=f"{antwoord}",
                    color=color_succes_fail,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=footer)
                await ctx.send(embed=em)
            else:
                await ctx.send(f"Je bent een te hoge prestige om nog te kunnen bedelen. (Prestige: {prestige[0]})")
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @bedel.error
    async def bedel_error(self, ctx, error):
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
    client.add_cog(EcoBedel(client))
