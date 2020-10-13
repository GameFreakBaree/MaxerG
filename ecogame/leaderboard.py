import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels


class EcoLeaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lb", "top"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def leaderboard(self, ctx, waarde=None, page=1):
        if str(ctx.channel) in ecogame_channels:
            doorgaan = True
            if waarde is None:
                index_waarde = 3
            elif waarde.lower() == "cash":
                index_waarde = 1
            elif waarde.lower() == "bank":
                index_waarde = 2
            elif waarde.lower() == "netto":
                index_waarde = 3
            else:
                try:
                    page = int(waarde)
                    index_waarde = 3
                except ValueError:
                    doorgaan = False

            if doorgaan:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                offset = (page - 1) * 10
                after_str = ""
                eerste_volgnummer = offset

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie ORDER BY netto DESC LIMIT 10 OFFSET {offset}")
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
                        pre_str = f"**{eerste_volgnummer}.** {top_names} • **€{geld}**\n"
                        after_str = after_str + pre_str

                if after_str == "":
                    after_str = "Geen data gevonden!"

                netto_totaal = 0
                maxergdb_cursor.execute(f"SELECT netto FROM maxerg_economie")
                cash_gegevens = maxergdb_cursor.fetchall()
                for row in cash_gegevens:
                    netto_totaal = netto_totaal + row[0]

                db_maxerg.close()

                embed = discord.Embed(
                    title=f"Leaderboard [Pagina {page}]",
                    description=f"__Totaal Geld:__ €{netto_totaal}\n\n{after_str}",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
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
    client.add_cog(EcoLeaderboard(client))
