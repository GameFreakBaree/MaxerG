import discord
from discord.ext import commands
import json
import datetime
import asyncio
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()


class EcoBalance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, *, member: discord.Member = None):
        ecogame_channels = ["💰│economy-game", "🔒│bots", "🔒│staff"]
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute("SELECT currency FROM maxerg_config")
            currency_tuple = maxergdb_cursor.fetchone()
            currency = currency_tuple[0]

            if member is None:
                member = ctx.author

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
            em.set_footer(text=embed_footer[0])
            await ctx.send(embed=em)
            db_maxerg.close()
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#708055327958106164> zitten om deze command uit te voeren.")
            await asyncio.sleep(3)
            await del_msg.delete()


def setup(client):
    client.add_cog(EcoBalance(client))
