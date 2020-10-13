import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency, ecogame_channels, prefix


class EcoShop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shop(self, ctx, setting=None, *, value=None):
        if str(ctx.channel) in ecogame_channels:
            if setting.lower() == "list" or setting is None:
                embed = discord.Embed(
                    title="Shop Lijst",
                    description=f"🐟 **Vishengel** ─ __€15.000__ ─ Tool\nVereist om de {prefix}fish command te gebruiken.\n\n"
                                f"🔒 **Slot** ─ __€50.000__ ─ Bescherming\n10% extra bescherming tegen de {prefix}rob command (Standaard: 40%)\n\n"
                                f"🔫 **Geweer** ─ __€75.000__ ─ Bescherming\n20% extra bescherming tegen de {prefix}rob command (Standaard: 40%)\n\n"
                                f"💣 **Bom** ─ __€2.500__ ─ Tool\n5% meer kans op slagen bij Crime & Rob command. [Werkt voor 1x per bom, Maximum 10 in inventory]\n\n"
                                f"<a:nitro_wumpus:760148768371900448> **Discord Nitro Classic** ─ __€1.000.000__ ─ Prijs (1 maand)\nMaximaal 1x claimen, beperkte voorraad!\n\n"
                                f"🤖 **100MB Bot Hosting 2** ─ __€500.000__ ─ Prijs (2 maanden)\nMaximaal 1x claimen, beperkte voorraad!\n\n"
                                f"🤖 **100MB Bot Hosting** ─ __€330.000__ ─ Prijs (1 maand)\nMaximaal 1x claimen, beperkte voorraad!\n\n"
                                f"🤖 **50MB Bot Hosting 2** ─ __€270.000__ ─ Prijs (2 maanden)\nMaximaal 1x claimen, beperkte voorraad!\n\n"
                                f"🤖 **50MB Bot Hosting** ─ __€150.000__ ─ Prijs (1 maand)\nMaximaal 1x claimen, beperkte voorraad!\n\n",
                    color=embedcolor
                )
                embed.set_thumbnail(url="https://i.imgur.com/MBI0iuV.png")
                embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text=f"{footer} | Pagina 1/1")
                await ctx.send(embed=embed)
            elif setting.lower() == "koop":
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                kopen = True
                extra = ""

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                eco_data = maxergdb_cursor.fetchone()
                cash = eco_data[1]

                maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_inventory WHERE user_id = {ctx.author.id}")
                user_id = maxergdb_cursor.fetchone()

                if user_id is None:
                    insert_new_inventory_user = "INSERT INTO maxerg_inventory (user_id, vishengel, slot, geweer, bom, nitro, hosting) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    inventory = (ctx.author.id, 0, 0, 0, 0, 0, 0)
                    maxergdb_cursor.execute(insert_new_inventory_user, inventory)
                    db_maxerg.commit()
                else:
                    maxergdb_cursor.execute(f"SELECT * FROM maxerg_inventory WHERE user_id = {ctx.author.id}")
                    inventory = maxergdb_cursor.fetchone()

                if value.lower() == "vishengel":
                    prijs = 15000
                    column_naam = "vishengel"
                    index = 1
                elif value.lower() == "slot":
                    prijs = 50000
                    column_naam = "slot"
                    index = 2
                elif value.lower() == "geweer":
                    prijs = 75000
                    column_naam = "geweer"
                    index = 3
                elif value.lower() == "bom":
                    kopen = False
                    if cash >= 2500:
                        if inventory[4] <= 10:
                            maxergdb_cursor.execute(f"UPDATE maxerg_inventory SET bom = bom + %s WHERE user_id = %s", (1, ctx.author.id))
                            maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - %s WHERE user_id = %s", (2500, ctx.author.id))
                            maxergdb_cursor.execute(f"UPDATE maxerg_economie SET netto = netto - %s WHERE user_id = %s", (2500, ctx.author.id))
                            db_maxerg.commit()

                            embed = discord.Embed(
                                title="Bom gekocht",
                                description=f"Je hebt succesvol een Bom gekocht.",
                                color=embedcolor
                            )
                            embed.set_thumbnail(url="https://i.imgur.com/MBI0iuV.png")
                            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                            embed.set_footer(text=footer)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"Je kunt niet meer dan 10 bommen kopen.")
                    else:
                        await ctx.send(f"Je hebt niet genoeg geld. Je hebt {currency}{cash}, je hebt {currency}2500 nodig.")
                elif value.lower() == "discord nitro classic":
                    prijs = 1000000
                    column_naam = "nitro"
                    index = 5
                    extra = "\nMaak een ticket aan in <#726058921881763911> om je prijs te claimen."
                elif value.lower() == "100mb bot hosting 2":
                    prijs = 500000
                    column_naam = "hosting"
                    index = 6
                    extra = "\nMaak een ticket aan in <#726058921881763911> om je prijs te claimen."
                elif value.lower() == "100mb bot hosting":
                    prijs = 330000
                    column_naam = "hosting"
                    index = 6
                    extra = "\nMaak een ticket aan in <#726058921881763911> om je prijs te claimen."
                elif value.lower() == "50mb bot hosting 2":
                    prijs = 270000
                    column_naam = "hosting"
                    index = 6
                    extra = "\nMaak een ticket aan in <#726058921881763911> om je prijs te claimen."
                elif value.lower() == "50mb bot hosting":
                    prijs = 150000
                    column_naam = "hosting"
                    index = 6
                    extra = "\nMaak een ticket aan in <#726058921881763911> om je prijs te claimen."
                else:
                    await ctx.send(f"Ongeldig Shop item. Doe `{prefix}shop list` om alle items te zien.")
                    kopen = False

                if kopen:
                    if cash >= prijs:
                        if inventory[index] == 0:
                            maxergdb_cursor.execute(f"UPDATE maxerg_inventory SET {column_naam} = %s WHERE user_id = %s", (1, ctx.author.id))
                            maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - %s WHERE user_id = %s", (prijs, ctx.author.id))
                            db_maxerg.commit()

                            embed = discord.Embed(
                                title=f"{value.title()} gekocht",
                                description=f"Je hebt succesvol een {value.title()} gekocht.{extra}",
                                color=embedcolor
                            )
                            embed.set_thumbnail(url="https://i.imgur.com/MBI0iuV.png")
                            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                            embed.set_footer(text=footer)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"Je hebt dit item al eens gekocht.")
                    else:
                        await ctx.send(f"Je hebt niet genoeg geld. Je hebt {currency}{cash}, je hebt {currency}{prijs} nodig.")
                else:
                    await ctx.send(f"Fout Argument. Doe `{prefix}shop koop <item>`. Om alle items te zien doe `{prefix}shop list")
                db_maxerg.close()
            else:
                await ctx.send(f"Fout Argument. Doe `{prefix}shop <list/koop>`.")
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")

    @shop.error
    async def shop_error(self, ctx, error):
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
    client.add_cog(EcoShop(client))
