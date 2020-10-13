import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels


class EcoBalance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, *, member: discord.Member = None):
        if str(ctx.channel) in ecogame_channels:
            if member is None:
                member = ctx.author

            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {member.id}")
            eco_data = maxergdb_cursor.fetchone()
            cash = eco_data[1]
            bank = eco_data[2]
            netto = eco_data[3]
            max_bank = eco_data[8]

            if cash is None or bank is None or max_bank is None:
                cash = 0
                bank = 0
                max_bank = 5000

            db_maxerg.close()

            em = discord.Embed(
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.add_field(name="Cash:", value=f"{currency}{cash}", inline=True)
            em.add_field(name="Bank:", value=f"{currency}{bank}/{max_bank}", inline=True)
            em.add_field(name="Totaal:", value=f"{currency}{netto}", inline=True)
            em.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @balance.error
    async def balance_error(self, ctx, error):
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
    client.add_cog(EcoBalance(client))
