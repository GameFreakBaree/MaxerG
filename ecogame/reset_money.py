import asyncio
import discord
from discord.ext import commands
import json
import datetime
import time
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()


class EcoResetMoney(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="reset-money")
    async def reset_money(self, ctx):
        ecogame_channels = ["💰│economy-game", "🔒│bots"]
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            em = discord.Embed(
                description=f"Wil je al je geld resetten? Type ` Ja ` als je al je geld wilt resetten.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer[0])
            embed = await ctx.send(embed=em)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "ja"

            try:
                await self.client.wait_for('message', check=check, timeout=60)

                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = 0 WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET bank = 0 WHERE user_id = {ctx.author.id}")
                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = 0 WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                em = discord.Embed(
                    description=f"Je hebt al je geld gereset!",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=embed_footer[0])
                await embed.edit(embed=em)
            except asyncio.TimeoutError:
                em = discord.Embed(
                    description="Geen reactie gekregen. Probeer het opnieuw.",
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=embed_footer[0])
                await embed.edit(embed=em)

            db_maxerg.close()
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#708055327958106164> zitten om deze command uit te voeren.")
            time.sleep(3)
            await del_msg.delete()


def setup(client):
    client.add_cog(EcoResetMoney(client))
