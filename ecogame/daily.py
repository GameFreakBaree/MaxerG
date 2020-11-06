import discord
from discord.ext import commands
import time
import datetime
import mysql.connector
from settings import host, user, password, database, footer, ecogame_channels, errorcolor, currency
from discord.utils import get


class EcoDaily(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            role_lvl5 = get(ctx.guild.roles, id=714036438659760159)
            role_lvl10 = get(ctx.guild.roles, id=714036464404398094)
            role_lvl20 = get(ctx.guild.roles, id=714036480724566057)
            role_lvl25 = get(ctx.guild.roles, id=714036496960847902)
            role_lvl30 = get(ctx.guild.roles, id=773957810135760956)

            if role_lvl30 in ctx.author.roles:
                doorgaan = True
                geld = 850
            elif role_lvl25 in ctx.author.roles:
                doorgaan = True
                geld = 650
            elif role_lvl20 in ctx.author.roles:
                doorgaan = True
                geld = 400
            elif role_lvl10 in ctx.author.roles:
                doorgaan = True
                geld = 250
            elif role_lvl5 in ctx.author.roles:
                doorgaan = True
                geld = 100
            else:
                doorgaan = False
                geld = 0

            if doorgaan:
                em = discord.Embed(
                    description=f"Je krijg **{currency}{geld}** vandaag!"
                                f"\nKom morgen terug om opnieuw deze bonus te claimen!",
                    color=0x1bd115
                )

                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {geld}, netto = netto + {geld} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()
            else:
                ctx.command.reset_cooldown(ctx)

                em = discord.Embed(
                    description=f"Je moet een rank hebben om dagelijks geld te claimen!\n"
                                f"Bekijk <#714116295175438457> om te zien welke ranks geld verdienen en hoeveel.",
                    color=0x1bd115
                )

            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 3600:
                conversion = time.strftime("%-Hu %-Mm %-Ss", time.gmtime(error.retry_after))
            else:
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
    client.add_cog(EcoDaily(client))
