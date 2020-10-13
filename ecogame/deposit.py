import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels


class EcoDeposit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["dep"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def deposit(self, ctx, amount=None):
        if str(ctx.channel) in ecogame_channels and amount is not None:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
            eco_data = maxergdb_cursor.fetchone()
            cash_currently = eco_data[1]
            bank_currently = eco_data[2]
            bank_max = eco_data[8]
            error_display = False

            if cash_currently is None:
                cash_currently = 0

            if amount == "all":
                if cash_currently > bank_max-bank_currently:
                    amount = bank_max-bank_currently
                else:
                    amount = cash_currently
            else:
                amount = int(amount)

            if amount > cash_currently or cash_currently <= 0:
                em = discord.Embed(
                    description=f"<:error:725030739531268187> Je kan dat bedrag niet overzetten naar de bank! Je hebt momenteel {currency}{cash_currently} in cash.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
            elif amount > bank_max - bank_currently or error_display is True:
                em = discord.Embed(
                    description=f"<:error:725030739531268187> Je hebt {currency}{bank_max - bank_currently} plaats op je bank.\n"
                                f"Doe `!prestige` om meer opslag te ontgrendelen.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
            else:
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {amount} WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET bank = bank + {amount} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                em = discord.Embed(
                    description=f"<:check:725030739543982240> {currency}{amount} overgezet naar de bank!",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {round(error.retry_after, 1)} seconden wachten om deze command opnieuw te gebruiken.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoDeposit(client))
