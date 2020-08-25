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

db_maxerg = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    passwd=password
)


class EcoLeaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lb", "top"])
    async def leaderboard(self, ctx, page=1):
        command_channels = ["💰│economy-game", "🔒│bots", "🔒│staff"]
        if str(ctx.channel) in command_channels:
            db_maxerg.commit()
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            pre_offset = page - 1
            offset = pre_offset * 10

            after_str = ""
            eerste_volgnummer = offset

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_ecogame ORDER BY netto DESC LIMIT 10 OFFSET {offset}")
            result = maxergdb_cursor.fetchall()
            for row in result:
                eerste_volgnummer = eerste_volgnummer + 1

                try:
                    top_name = self.client.get_user(row[0])
                    top_names = top_name.mention
                except AttributeError:
                    top_names = row[0]

                top_aantal_berichten = row[3]

                pre_str = f"**{eerste_volgnummer}.** {top_names} • **€{top_aantal_berichten}**\n"
                after_str = after_str + pre_str

            if after_str == "":
                after_str = "Geen data gevonden!"

            alle_cash = 0
            maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame")
            cash_gegevens = maxergdb_cursor.fetchall()
            for row in cash_gegevens:
                alle_cash = alle_cash + row[0]

            alle_bank = 0
            maxergdb_cursor.execute(f"SELECT bank FROM maxerg_ecogame")
            bank_gegevens = maxergdb_cursor.fetchall()
            for row in bank_gegevens:
                alle_bank = alle_bank + row[0]

            alle_berichten = alle_cash + alle_bank

            embed = discord.Embed(
                title=f"Leaderboard [Pagina {page}]",
                description=f"__Totaal Geld:__ €{alle_berichten}\n\n{after_str}",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#747575812605214900> zitten om deze command uit te voeren.")
            time.sleep(3)
            await del_msg.delete()


def setup(client):
    client.add_cog(EcoLeaderboard(client))
