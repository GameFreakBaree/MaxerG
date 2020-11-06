import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels, currency, prefix


class EcoPrestige(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
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
                elif prestige == 1 and cash >= 12000:
                    bedrag = 12000
                    max_bank = 20000
                elif prestige == 2 and cash >= 18000:
                    bedrag = 18000
                    max_bank = 35000
                elif prestige == 3 and cash >= 26000:
                    bedrag = 26000
                    max_bank = 60000
                elif prestige == 4 and cash >= 35000:
                    bedrag = 35000
                    max_bank = 80000
                elif prestige == 5 and cash >= 48000:
                    bedrag = 48000
                    max_bank = 130000
                elif prestige == 6 and cash >= 60000:
                    bedrag = 60000
                    max_bank = 175000
                elif prestige == 7 and cash >= 72000:
                    bedrag = 72000
                    max_bank = 250000
                elif prestige == 8 and cash >= 90000:
                    bedrag = 90000
                    max_bank = 300000
                elif prestige == 9 and cash >= 100000:
                    bedrag = 100000
                    max_bank = 360000
                elif prestige == 10 and cash >= 112000:
                    bedrag = 112000
                    max_bank = 420000
                elif prestige == 11 and cash >= 125000:
                    bedrag = 125000
                    max_bank = 500000
                elif prestige == 12:
                    await ctx.send(f"Je bent al maximum prestige!")
                    doorgaan = False
                else:
                    await ctx.send(f"Je hebt niet genoeg geld om te prestigen.\nDoe `{prefix}prestige info` om te zien hoeveel het kost.")
                    doorgaan = False

                if doorgaan:
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET prestige = prestige+1, max_bank = {max_bank} WHERE user_id = {ctx.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {bedrag}, netto = netto - {bedrag} WHERE user_id = {ctx.author.id}")
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
                    description=f"**Wat Is Prestigen?**\nDankzij prestigen kan je hogere jobs ontgrendelen. Bij elke prestige krijg je meer opslag in je bank.\n\n"
                                f"**Welke voordelen krijg ik per level?**"
                                f"\n• __Prestige 0 (standaard)__ ─ __Prijs:__ {currency}0 ─ Bank Opslag: {currency}5.000, Jobs: 1"
                                f"\n• __Prestige 1__ ─ __Prijs:__ {currency}8.000 ─ Opslag: {currency}10.000, Jobs: 2"
                                f"\n• __Prestige 2__ ─ __Prijs:__ {currency}12.000 ─ Opslag: {currency}20.000, Jobs: 3"
                                f"\n• __Prestige 3__ ─ __Prijs:__ {currency}18.000 ─ Opslag: {currency}35.000, Jobs: 4"
                                f"\n• __Prestige 4__ ─ __Prijs:__ {currency}26.000 ─ Opslag: {currency}60.000, Jobs: 5"
                                f"\n• __Prestige 5__ ─ __Prijs:__ {currency}35.000 ─ Opslag: {currency}80.000, Jobs: 6"
                                f"\n• __Prestige 6__ ─ __Prijs:__ {currency}48.000 ─ Opslag: {currency}130.000, Jobs: 7"
                                f"\n• __Prestige 7__ ─ __Prijs:__ {currency}60.000 ─ Opslag: {currency}175.000, Jobs: 8"
                                f"\n• __Prestige 8__ ─ __Prijs:__ {currency}72.000 ─ Opslag: {currency}250.000, Jobs: 9"
                                f"\n• __Prestige 9__ ─ __Prijs:__ {currency}90.000 ─ Opslag: {currency}300.000, Jobs: 10"
                                f"\n• __Prestige 10__ ─ __Prijs:__ {currency}100.000 ─ Opslag: {currency}360.000, Jobs: 11"
                                f"\n• __Prestige 11__ ─ __Prijs:__ {currency}112.000 ─ Opslag: {currency}420.000, Jobs: 12"
                                f"\n• __Prestige 12__ ─ __Prijs:__ {currency}125.000 ─ Opslag: {currency}500.000, Jobs: 13",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoPrestige(client))
