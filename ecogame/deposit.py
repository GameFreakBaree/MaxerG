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


class EcoDeposit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):
        ecogame_channels = ["💰│economy-game", "🔒│bots"]
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

            if amount is not None:
                maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {ctx.author.id}")
                cash_currently_tuple = maxergdb_cursor.fetchone()
                if cash_currently_tuple is None:
                    cash_currently = 0
                else:
                    cash_currently = cash_currently_tuple[0]

                if amount == "all":
                    amount = cash_currently
                else:
                    amount = int(amount)

                if amount > cash_currently or cash_currently <= 0:
                    em = discord.Embed(
                        description=f"<:error:725030739531268187> Je kan dat bedrag niet overzetten naar de bank! Je hebt momenteel {currency}{cash_currently} in cash.",
                        color=embed_color,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    em.set_footer(text=embed_footer[0])
                    await ctx.send(embed=em)
                else:
                    maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash - {amount} WHERE user_id = {ctx.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET bank = bank + {amount} WHERE user_id = {ctx.author.id}")
                    db_maxerg.commit()

                    em = discord.Embed(
                        description=f"<:check:725030739543982240> {currency}{amount} overgezet naar de bank!",
                        color=embed_color,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    em.set_footer(text=embed_footer[0])
                    await ctx.send(embed=em)
            else:
                await ctx.send("Voer een geldig bedrag in.")

            db_maxerg.close()
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#708055327958106164> zitten om deze command uit te voeren.")
            await asyncio.sleep(3)
            await del_msg.delete()


def setup(client):
    client.add_cog(EcoDeposit(client))
