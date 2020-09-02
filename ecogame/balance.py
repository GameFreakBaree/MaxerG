import discord
from discord.ext import commands
import json
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


class EcoBalance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, *, member: discord.Member = None):
        ecogame_channels = ["💰│economy-game", "🔒│bots", "🔒│staff"]
        if str(ctx.channel) in ecogame_channels:
            if member is None:
                member = ctx.author

            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {member.id}")
            cash = maxergdb_cursor.fetchone()
            if cash is None:
                cash = (0,)

            maxergdb_cursor.execute(f"SELECT bank FROM maxerg_ecogame WHERE user_id = {member.id}")
            bank = maxergdb_cursor.fetchone()
            if bank is None:
                bank = (0,)

            net_worth = cash[0] + bank[0]

            em = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.add_field(name="Cash:", value=f"{currency}{cash[0]}", inline=True)
            em.add_field(name="Bank:", value=f"{currency}{bank[0]}", inline=True)
            em.add_field(name="Net Worth:", value=f"{currency}{net_worth}", inline=True)
            em.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
            em.set_footer(text=embed_footer)
            await ctx.send(embed=em)
            db_maxerg.close()


def setup(client):
    client.add_cog(EcoBalance(client))
