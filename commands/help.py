import discord
from discord.ext import commands
import json
import datetime

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

prefix = settings['prefix']
currency = settings['currency']
embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()

embed_color = int(embedcolor, 16)


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
                            f"\n• {prefix}help - Bekijk deze embed!"
                            f"\n• {prefix}info @<naam> - Zie info over de getagde speler"
                            f"\n• {prefix}rank @<naam>- Zie jouw rank in deze server."
                            f"\n• {prefix}levels - Bekijk het hele level scoreboard."
                            f"\n• {prefix}members - Bekijk hoeveel leden er in {ctx.guild.name} zitten."
                            f"\n\n__**Ticket Commands**__\n"
                            f"\n• {prefix}new - Maak een Ticket aan."
                            f"\n• {prefix}close - Verwijder je Ticket."
                            f"\n• {prefix}add - Voeg iemand aan je Ticket toe."
                            f"\n• {prefix}remove - Verwijder iemand van je Ticket."
                            f"\n\n__**Economy Commands**__\n"
                            f"\n• {prefix}help - Bekijk alle commands in <#708055327958106164>."
                            f"\n• {prefix}lb - Bekijk het hele ecogame scoreboard."
                            f"\n• {prefix}with <bedrag> of !with all - Haal een bedrag af van de bank."
                            f"\n• {prefix}dep <bedrag> of !dep all - Zet een bedrag op de bank."
                            f"\n• {prefix}reset_money - Reset je geld naar {currency}0."
                            f"\n• {prefix}work - Verdien geld met deze command."
                            f"\n• {prefix}slut - Verdien geld of verlies met deze command."
                            f"\n• {prefix}crime - Verdien geld of verlies met deze command."
                            f"\n• {prefix}rob <naam> - Steel alle cash van een speler."
                            f"\n• {prefix}game blackjack <inzet> - Speel blackjack."
                            f"\n• {prefix}game russian-roulette <inzet> - Speel Russian Roueltte."
                            f"\n• {prefix}game roulette <inzet> <space> - Speel Roulette."
                            f"\n\n__**Fun Commands**__\n"
                            f"\n• {prefix}rps - Speel Steen Papier Schaar met de bot."
                            f"\n• {prefix}wyr - Krijg een Would You Rather vraag."
                            f"\n• {prefix}fact - Krijg een willekeurig weetje te zien."
                            f"\n• {prefix}8ball - Vraag de magische 8ball een vraag."
                            f"\n• {prefix}coinflip - Wordt het kop of munt?"
                            f"\n• {prefix}nhie- Speel Never Have I Ever met de bot.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            help_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            help_embed.set_thumbnail(url=self.client.user.avatar_url)
            help_embed.set_footer(text=embed_footer)
            await ctx.send(embed=help_embed)
        elif str(ctx.channel) in ecogame_channels:
            #                "\n__Failrate:__ 25%\n__Cooldown:__ 2 uur\n\n`/blackjack [Bet]`\n__Min Bet:__ €15"
            #                "\n__Max Bet:__ €750\n__Cooldown:__ 20 Games per uur\n\n`/roulette [Bet] [Space]`"
            #                "\n__Min Bet:__ €50\n__Max Bet:__ €1000\n__Cooldown:__ 20 Games per uur\n\n"
            #                "`/slot-machine [Bet]`\n__Min Bet:__ €10\n__Max Bet:__ €500"
            #                "\n__Cooldown:__ 20 Games per uur\n\n`/cock-fight [Bet]`\n__Min Bet:__ €5"
            #                "\n__Max Bet:__ €200\n__Cooldown:__ 20 Games per uur\n\n`/russian-roulette [Bet]`"
            #                "\n__Min Bet:__ €50\n__Max Bet:__ €800\n__Cooldown:__ 20 Games per uur\n\n```fix"
            await ctx.send(
                f"```fix\nAlle Commands```"
                f"\n`!work`"
                f"\n__Payout:__ {currency}6 - {currency}25"
                f"\n__Failrate:__ 0%"
                f"\n__Cooldown:__ 60 minuten\n"
                f"\n`!crime`"
                f"\n__Payout:__ {currency}250 - {currency}500"
                f"\n__Failrate:__ 75%"
                f"\n__Cooldown:__ 24 uur\n"
                f"\n`!rob [NAAM]`"
                f"\n__Payout:__ Alle Cash van die speler"
                f"\n__Failrate:__ 50%"
                f"\n__Cooldown:__ 12 uur\n"
                f"\n`!slut`"
                f"\n__Payout:__ {currency}30 - {currency}60"
                f"\n__Failrate:__ 25%"
                f"\n__Cooldown:__ 2 uur\n"
                f"\n```fix"
                f"\nGeneral Commands```"
                f"\n`!with [Amount]` of `!with all`"
                f"\n`!dep [Amount]` of `!dep all`"
                f"\n`!top` of `!lb` - Bekijk het hele scorebord."
                f"\n`!help` - Bekijk deze lijst."
                f"\n`!reset-money` - Reset je geld naar {currency}0."
            )


def setup(client):
    client.add_cog(Commands(client))
