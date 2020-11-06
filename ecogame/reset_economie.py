import asyncio
import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels


class EcoResetMoney(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="reset-economie")
    async def reset_economie(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            em = discord.Embed(
                description=f"Wil je al je voortgang resetten? Type ` Ja `.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            embed = await ctx.send(embed=em)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "ja"

            try:
                await self.client.wait_for('message', check=check, timeout=60)

                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"DELETE FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()
                db_maxerg.close()

                em = discord.Embed(
                    description=f"Je hebt al je voortgang gereset!",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=footer)
                await embed.edit(embed=em)
            except asyncio.TimeoutError:
                em = discord.Embed(
                    description="Geen reactie gekregen. Probeer het opnieuw.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                em.set_footer(text=footer)
                await embed.edit(embed=em)
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoResetMoney(client))
