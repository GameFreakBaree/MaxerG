import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels, prefix


class EcoPay(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['give'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pay(self, ctx, amount=None, *, member: discord.Member = None):
        if str(ctx.channel) in ecogame_channels:
            if amount is not None and member is not None and member != ctx.author:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                eco_data_sender = maxergdb_cursor.fetchone()
                cash_currently = eco_data_sender[1]

                if amount > cash_currently:
                    await ctx.send(f"Je hebt maar {currency}{cash_currently}.")
                else:
                    maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {member.id}")
                    eco_data_receiver = maxergdb_cursor.fetchone()

                    if eco_data_receiver is None:
                        await ctx.send(f"Deze gebruiker staat niet in onze database. Zorg dat hij iets stuurt of even `{prefix}bedel` doet.")
                    else:
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {amount} WHERE user_id = {ctx.author.id}")
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto - {amount} WHERE user_id = {ctx.author.id}")
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {amount} WHERE user_id = {member.id}")
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto + {amount} WHERE user_id = {member.id}")
                        db_maxerg.commit()

                        em = discord.Embed(
                            description=f"<:check:725030739543982240> Je hebt {currency}{amount} gegeven aan {member}!",
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        em.set_footer(text=footer)
                        await ctx.send(embed=em)
                    db_maxerg.close()
            else:
                await ctx.send(f"Ongeldige Argumenten. Voorbeeld`{prefix}pay 100 GameFreakBaree#9999`")
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")

    @pay.error
    async def pay_error(self, ctx, error):
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
    client.add_cog(EcoPay(client))
