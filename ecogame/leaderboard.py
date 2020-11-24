import discord
from discord.ext import commands
import datetime
import mysql.connector
import asyncio
from settings import host, user, password, database, embedcolor, footer, ecogame_channels, currency


class EcoLeaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lb", "top"])
    async def leaderboard(self, ctx, waarde=None, page=1):
        if str(ctx.channel) in ecogame_channels:
            doorgaan = True
            prefix = "Totaal Geld"
            lengte_woord = len(prefix)

            if waarde is None:
                index_waarde = 3
                waarde = "netto"
            elif waarde.lower() == "cash":
                index_waarde = 1
                prefix = "Totaal Cash"
                lengte_woord = len(prefix)
            elif waarde.lower() == "bank":
                index_waarde = 2
                prefix = "Totaal Bank"
                lengte_woord = len(prefix)
            elif waarde.lower() == "netto":
                index_waarde = 3
                lengte_woord = len(prefix)
            elif waarde.lower() == "prestige":
                index_waarde = 4
                prefix = "Prestige"
                lengte_woord = len(prefix)
            else:
                index_waarde = 3
                try:
                    page = int(waarde)
                except ValueError:
                    doorgaan = False

            if doorgaan:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                offset = (page - 1) * 10
                volgnummer = offset
                leaderboard_zin = ""
                langste_regel = 0

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie ORDER BY {waarde.lower()} DESC LIMIT 10 OFFSET {offset}")
                result = maxergdb_cursor.fetchall()
                for row in result:
                    volgnummer = volgnummer + 1
                    volgnummer_prefix = f"{volgnummer}."
                    lengte_volgnummer_prefix = len(volgnummer_prefix)
                    aantal_spaties = 4 - lengte_volgnummer_prefix
                    spatie_prefix = " " * aantal_spaties
                    volgnummer_prefix = spatie_prefix + volgnummer_prefix

                    try:
                        top_names = self.client.get_user(row[0])
                    except AttributeError:
                        top_names = "Onbekend#0000"

                    geld = row[index_waarde]
                    if index_waarde == 4:
                        geld = f"{geld}"
                    else:
                        geld = f"{currency}{geld}"
                    lengte_geld = len(str(geld))
                    aantal_spaties = lengte_woord - lengte_geld
                    spatie_prefix = " " * aantal_spaties
                    geld_prefix = spatie_prefix + str(geld)

                    if geld != 0:
                        nieuwe_zin = f"{volgnummer_prefix} | {geld_prefix} | {top_names}\n"
                        leaderboard_zin = leaderboard_zin + nieuwe_zin

                        if len(nieuwe_zin) > langste_regel:
                            langste_regel = len(nieuwe_zin)

                if leaderboard_zin == "":
                    leaderboard_zin = "Geen data gevonden!"

                netto_totaal = 0
                maxergdb_cursor.execute(f"SELECT netto FROM maxerg_economie")
                cash_gegevens = maxergdb_cursor.fetchall()
                for row in cash_gegevens:
                    netto_totaal = netto_totaal + row[0]

                maxergdb_cursor.execute(f"SELECT {waarde.lower()} FROM maxerg_economie WHERE {waarde.lower()} != 0")
                max_pages_tuple = maxergdb_cursor.fetchall()

                max_pages = len(max_pages_tuple)

                if max_pages % 10 != 0:
                    max_pages = max_pages // 10 + 1
                else:
                    max_pages = max_pages // 10

                header = f"Rank | {prefix} | Gebruiker"

                if len(header) > langste_regel:
                    langste_regel = len(header)

                seperator = "=" * langste_regel

                embed = discord.Embed(
                    title=f"Leaderboard",
                    description=f"```md\n{header}\n{seperator}\n{leaderboard_zin}\n```",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=f"{footer} | Pagina {page}/{max_pages}")
                leaderboard_message = await ctx.send(embed=embed)

                await leaderboard_message.add_reaction("◀️")
                await leaderboard_message.add_reaction("▶️")

                def check(reaction, member):
                    return member == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

                while True:
                    try:
                        reaction, member = await self.client.wait_for("reaction_add", timeout=30, check=check)

                        if str(reaction.emoji) == "▶️" and page != max_pages:
                            page += 1
                            await leaderboard_message.remove_reaction(reaction, member)
                            nieuwe_pagina = True
                        elif str(reaction.emoji) == "◀️" and page > 1:
                            page -= 1
                            await leaderboard_message.remove_reaction(reaction, member)
                            nieuwe_pagina = True
                        else:
                            await leaderboard_message.remove_reaction(reaction, member)
                            nieuwe_pagina = False

                        if nieuwe_pagina:
                            offset = (page - 1) * 10
                            leaderboard_zin = ""
                            volgnummer = offset

                            maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie ORDER BY {waarde.lower()} DESC LIMIT 10 OFFSET {offset}")
                            result = maxergdb_cursor.fetchall()
                            for row in result:
                                volgnummer = volgnummer + 1
                                volgnummer_prefix = f"{volgnummer}."
                                lengte_volgnummer_prefix = len(volgnummer_prefix)
                                aantal_spaties = 4 - lengte_volgnummer_prefix
                                spatie_prefix = " " * aantal_spaties
                                volgnummer_prefix = spatie_prefix + volgnummer_prefix

                                try:
                                    top_names = self.client.get_user(row[0])
                                except AttributeError:
                                    top_names = "Onbekend#0000"

                                geld = row[index_waarde]
                                if index_waarde == 4:
                                    geld = f"{geld}"
                                else:
                                    geld = f"{currency}{geld}"
                                lengte_geld = len(str(geld))
                                aantal_spaties = lengte_woord - lengte_geld
                                spatie_prefix = " " * aantal_spaties
                                geld_prefix = spatie_prefix + str(geld)

                                if geld != 0:
                                    nieuwe_zin = f"{volgnummer_prefix} | {geld_prefix} | {top_names}\n"
                                    leaderboard_zin = leaderboard_zin + nieuwe_zin

                                    if len(nieuwe_zin) > langste_regel:
                                        langste_regel = len(nieuwe_zin)

                            if leaderboard_zin == "":
                                leaderboard_zin = "Geen data gevonden!"

                            if len(header) > langste_regel:
                                langste_regel = len(header)

                            seperator = "=" * langste_regel

                            embed = discord.Embed(
                                title=f"Leaderboard",
                                description=f"```md\n{header}\n{seperator}\n{leaderboard_zin}\n```",
                                color=embedcolor,
                                timestamp=datetime.datetime.utcnow()
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer} | Pagina {page}/{max_pages}")
                            await leaderboard_message.edit(embed=embed)
                    except asyncio.TimeoutError:
                        await leaderboard_message.clear_reaction("◀️")
                        await leaderboard_message.clear_reaction("▶️")
                        break

                db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoLeaderboard(client))
