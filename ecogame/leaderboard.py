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
            prefix = currency
            if waarde is None:
                index_waarde = 3
                waarde = "netto"
            elif waarde.lower() == "cash":
                index_waarde = 1
            elif waarde.lower() == "bank":
                index_waarde = 2
            elif waarde.lower() == "netto":
                index_waarde = 3
            elif waarde.lower() == "prestige":
                index_waarde = 4
                prefix = "Prestige: "
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
                after_str = ""
                eerste_volgnummer = offset

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie ORDER BY {waarde.lower()} DESC LIMIT 10 OFFSET {offset}")
                result = maxergdb_cursor.fetchall()
                for row in result:
                    eerste_volgnummer = eerste_volgnummer + 1

                    try:
                        top_name = self.client.get_user(row[0])
                        top_names = top_name.mention
                    except AttributeError:
                        top_names = row[0]

                    geld = row[index_waarde]

                    if geld != 0:
                        pre_str = f"**{eerste_volgnummer}.** {top_names} • **{prefix}{geld}**\n"
                        after_str = after_str + pre_str

                if after_str == "":
                    after_str = "Geen data gevonden!"

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

                embed = discord.Embed(
                    title=f"Leaderboard [Pagina {page}/{max_pages}]",
                    description=f"__Totaal Geld:__ €{netto_totaal}\n\n{after_str}",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
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
                            after_str = ""
                            eerste_volgnummer = offset

                            maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie ORDER BY {waarde.lower()} DESC LIMIT 10 OFFSET {offset}")
                            result = maxergdb_cursor.fetchall()
                            for row in result:
                                eerste_volgnummer = eerste_volgnummer + 1

                                try:
                                    top_name = self.client.get_user(row[0])
                                    top_names = top_name.mention
                                except AttributeError:
                                    top_names = row[0]

                                geld = row[index_waarde]

                                if geld != 0:
                                    pre_str = f"**{eerste_volgnummer}.** {top_names} • **{prefix}{geld}**\n"
                                    after_str = after_str + pre_str

                            if after_str == "":
                                after_str = "Geen data gevonden!"

                            embed = discord.Embed(
                                title=f"Leaderboard [Pagina {page}/{max_pages}]",
                                description=f"__Totaal Geld:__ €{netto_totaal}\n\n{after_str}",
                                color=embedcolor,
                                timestamp=datetime.datetime.utcnow()
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=footer)
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
