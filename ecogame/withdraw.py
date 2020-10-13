import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels


class EcoWithdraw(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["with"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        if str(ctx.channel) in ecogame_channels:
            if amount is not None:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT bank FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                geld_currently_tuple = maxergdb_cursor.fetchone()
                if geld_currently_tuple is None:
                    geld_currently = 0
                else:
                    geld_currently = geld_currently_tuple[0]

                if amount == "all":
                    amount = geld_currently
                else:
                    amount = int(amount)

                if amount > geld_currently or geld_currently <= 0:
                    em = discord.Embed(
                        description=f"<:error:725030739531268187> Je kan dat bedrag niet afhalen van de bank! Je hebt momenteel {currency}{geld_currently} op je bankrekening.",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                else:
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET bank = bank - {amount} WHERE user_id = {ctx.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {amount} WHERE user_id = {ctx.author.id}")
                    db_maxerg.commit()

                    em = discord.Embed(
                        description=f"<:check:725030739543982240> {currency}{amount} afgehaald van de bank!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=footer)
                await ctx.send(embed=em)
                db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @withdraw.error
    async def withdraw_error(self, ctx, error):
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
    client.add_cog(EcoWithdraw(client))
