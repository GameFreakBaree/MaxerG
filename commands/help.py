import discord
from discord.ext import commands
import json
import datetime
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

maxergdb_cursor = db_maxerg.cursor()

maxergdb_cursor.execute("SELECT prefix FROM maxerg_config")
prefix = maxergdb_cursor.fetchone()

maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
embed_color_tuple = maxergdb_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)

maxergdb_cursor.execute("SELECT currency FROM maxerg_config")
currency = maxergdb_cursor.fetchone()

maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
embed_footer = maxergdb_cursor.fetchone()


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="commands", aliases=["help"])
    async def commands_help(self, ctx):
        command_channels = ["🤖│commands", "🔒│bots"]
        ecogame_channels = ["💰│economy-game"]
        if str(ctx.channel) in command_channels:
            help_embed = discord.Embed(
                title="Alle Commands",
                description=f"__**Algemene Commands**__\n"
                            f"\n• {prefix[0]}help - Bekijk deze embed!"
                            f"\n• {prefix[0]}info @<naam> - Zie info over de getagde speler"
                            f"\n• {prefix[0]}rank @<naam>- Zie jouw rank in deze server."
                            f"\n• {prefix[0]}levels - Bekijk het hele level scoreboard."
                            f"\n• {prefix[0]}members - Bekijk hoeveel leden er in {ctx.guild.name} zitten."
                            f"\n\n__**Ticket Commands**__\n"
                            f"\n• {prefix[0]}new - Maak een Ticket aan."
                            f"\n• {prefix[0]}close - Verwijder je Ticket."
                            f"\n• {prefix[0]}add - Voeg iemand aan je Ticket toe."
                            f"\n• {prefix[0]}remove - Verwijder iemand van je Ticket."
                            f"\n\n__**Economy Commands**__\n"
                            f"\n• {prefix[0]}help - Bekijk alle commands in <#742737319177617430>."
                            f"\n• {prefix[0]}lb - Bekijk het hele ecogame scoreboard."
                            f"\n• {prefix[0]}with <bedrag> of !with all - Haal een bedrag af van de bank."
                            f"\n• {prefix[0]}dep <bedrag> of !dep all - Zet een bedrag op de bank."
                            f"\n• {prefix[0]}reset_money - Reset je geld naar {currency[0]}0."
                            f"\n• {prefix[0]}work - Verdien geld met deze command."
                            f"\n• {prefix[0]}slut - Verdien geld of verlies met deze command."
                            f"\n• {prefix[0]}crime - Verdien geld of verlies met deze command."
                            f"\n• {prefix[0]}rob <naam> - Steel alle cash van een speler."
                            f"\n• {prefix[0]}game blackjack <inzet> - Speel blackjack."
                            f"\n• {prefix[0]}game russian-roulette <inzet> - Speel Russian Roueltte."
                            f"\n• {prefix[0]}game roulette <inzet> <space> - Speel Roulette."
                            f"\n\n__**Fun Commands**__\n"
                            f"\n• {prefix[0]}rps - Speel Steen Papier Schaar met de bot."
                            f"\n• {prefix[0]}wyr - Krijg een Would You Rather vraag."
                            f"\n• {prefix[0]}fact - Krijg een willekeurig weetje te zien."
                            f"\n• {prefix[0]}8ball - Vraag de magische 8ball een vraag."
                            f"\n• {prefix[0]}coinflip - Wordt het kop of munt?"
                            f"\n• {prefix[0]}nhie- Speel Never Have I Ever met de bot.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            help_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            help_embed.set_thumbnail(url=self.client.user.avatar_url)
            help_embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=help_embed)
        elif str(ctx.channel) in ecogame_channels:
            await ctx.send(
                f"```fix\nAlle Commands```"
                f"\n`!work`"
                f"\n__Payout:__ {currency[0]}6 - {currency[0]}25"
                f"\n__Failrate:__ 0%"
                f"\n__Cooldown:__ 60 minuten\n"
                f"\n`!crime`"
                f"\n__Payout:__ {currency[0]}250 - {currency[0]}500"
                f"\n__Failrate:__ 75%"
                f"\n__Cooldown:__ 24 uur\n"
                f"\n`!rob [NAAM]`"
                f"\n__Payout:__ Alle Cash van die speler"
                f"\n__Failrate:__ 50%"
                f"\n__Cooldown:__ 12 uur\n"
                f"\n`!slut`"
                f"\n__Payout:__ {currency[0]}30 - {currency[0]}60"
                f"\n__Failrate:__ 25%"
                f"\n__Cooldown:__ 2 uur\n"
                f"\n```fix"
                f"\nGeneral Commands```"
                f"\n`!with [Amount]` of `!with all`"
                f"\n`!dep [Amount]` of `!dep all`"
                f"\n`!top` of `!lb` - Bekijk het hele scorebord."
                f"\n`!help` - Bekijk deze lijst."
                f"\n`!reset-money` - Reset je geld naar {currency[0]}0."
            )


def setup(client):
    client.add_cog(Commands(client))
