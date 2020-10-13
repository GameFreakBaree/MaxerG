import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels, currency, prefix


class EcoPrestige(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def prestige(self, ctx, info=None):
        if str(ctx.channel) in ecogame_channels:
            if info is None:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                eco_data = maxergdb_cursor.fetchone()
                prestige = eco_data[4]
                cash = eco_data[1]

                doorgaan = True
                if prestige == 0 and cash >= 8000:
                    bedrag = 8000
                    max_bank = 10000
                elif prestige == 1 and cash >= 20000:
                    bedrag = 20000
                    max_bank = 20000
                elif prestige == 2 and cash >= 35000:
                    bedrag = 35000
                    max_bank = 30000
                elif prestige == 3 and cash >= 50000:
                    bedrag = 50000
                    max_bank = 50000
                elif prestige == 4 and cash >= 70000:
                    bedrag = 70000
                    max_bank = 75000
                elif prestige == 5 and cash >= 90000:
                    bedrag = 90000
                    max_bank = 100000
                elif prestige == 6 and cash >= 110000:
                    bedrag = 110000
                    max_bank = 150000
                elif prestige == 7 and cash >= 150000:
                    bedrag = 150000
                    max_bank = 200000
                elif prestige == 8:
                    await ctx.send(f"Je bent al maximum prestige!")
                    doorgaan = False
                else:
                    await ctx.send(f"Je hebt niet genoeg geld om te prestigen.\nDoe `{prefix}prestige info` om te zien hoeveel het kost.")
                    doorgaan = False
                    ctx.command.reset_cooldown(ctx)

                if doorgaan:
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET prestige = prestige+1 WHERE user_id = {ctx.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {bedrag} WHERE user_id = {ctx.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto - {bedrag} WHERE user_id = {ctx.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET max_bank = {max_bank} WHERE user_id = {ctx.author.id}")
                    db_maxerg.commit()

                    embed = discord.Embed(
                        title="Prestige Omhoog",
                        description=f"{ctx.author.mention} is nu prestige {prestige+1}!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_thumbnail(url="https://i.imgur.com/iGRoyjn.png")
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)
                db_maxerg.close()
            else:
                embed = discord.Embed(
                    title=f"Prestige Info",
                    description=f"**Wat Is Prestigen?**\nDankzij prestigen kan je hogere jobs ontgrendelen. Bij elke prestige kan je ook meer geld opslag in je bank.\n\n"
                                f"**Welke Voordelen Krijg ik per level?**"
                                f"\n• __Prestige 0 (standaard)__ ─ __Prijs:__ {currency}0 ─ Bank Opslag: {currency}5.000, Jobs: 2"
                                f"\n• __Prestige 1__ ─ __Prijs:__ {currency}8.000 ─ Bank Opslag: {currency}10.000, Jobs: 3"
                                f"\n• __Prestige 2__ ─ __Prijs:__ {currency}20.000 ─ Bank Opslag: {currency}20.000, Jobs: 4"
                                f"\n• __Prestige 3__ ─ __Prijs:__ {currency}35.000 ─ Bank Opslag: {currency}30.000, Jobs: 5"
                                f"\n• __Prestige 4__ ─ __Prijs:__ {currency}50.000 ─ Bank Opslag: {currency}50.000, Jobs: 6"
                                f"\n• __Prestige 5__ ─ __Prijs:__ {currency}70.000 ─ Bank Opslag: {currency}75.000, Jobs: 7"
                                f"\n• __Prestige 6__ ─ __Prijs:__ {currency}90.000 ─ Bank Opslag: {currency}100.000, Jobs: 8"
                                f"\n• __Prestige 7__ ─ __Prijs:__ {currency}110.000 ─ Bank Opslag: {currency}150.000, Jobs: 9"
                                f"\n• __Prestige 8__ ─ __Prijs:__ {currency}150.000 ─ Bank Opslag: {currency}200.000, Jobs: 10",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @prestige.error
    async def prestige_error(self, ctx, error):
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
    client.add_cog(EcoPrestige(client))
