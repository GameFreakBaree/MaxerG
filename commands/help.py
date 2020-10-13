import discord
from discord.ext import commands
import datetime
from settings import prefix, currency, embedcolor, footer, command_channels, ecogame_channels


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="commands", aliases=["help"])
    async def commands_help(self, ctx):
        if str(ctx.channel) in command_channels:
            help_embed = discord.Embed(
                title="Alle Commands",
                description=f"__**Algemene Commands**__\n"
                            f"\n• **{prefix}help** - Bekijk deze embed!"
                            f"\n• **{prefix}info @<naam>** - Zie info over de getagde speler"
                            f"\n• **{prefix}rank @<naam>** - Zie jouw rank in deze server."
                            f"\n• **{prefix}levels** - Bekijk het hele level scoreboard."
                            f"\n• **{prefix}members** - Bekijk hoeveel leden er in {ctx.guild.name} zitten."
                            f"\n• **{prefix}ping** of **{prefix}uptime** - Bekijk de ping en uptime van de bot."
                            f"\n• **{prefix}ip** - Bekijk het IP van de server."
                            f"\n\n__**Ticket Commands**__\n"
                            f"\n• **{prefix}close** - Verwijder je Ticket."
                            f"\n• **{prefix}add** - Voeg iemand aan je Ticket toe."
                            f"\n• **{prefix}remove** - Verwijder iemand van je Ticket."
                            f"\n\n__**Economy Commands**__\n"
                            f"\n__Doe__ `{prefix}help` __in__ <#708055327958106164> __om de commands te zien.__"
                            f"\n\n__**Fun Commands**__\n"
                            f"\n• **{prefix}rps <steen/papier/schaar>** - Speel Steen Papier Schaar met de bot."
                            f"\n• **{prefix}wyr** - Krijg een Would You Rather vraag."
                            f"\n• **{prefix}fact** - Krijg een willekeurig weetje te zien."
                            f"\n• **{prefix}8ball <vraag>** - Vraag de magische 8ball een vraag."
                            f"\n• **{prefix}coinflip** - Wordt het kop of munt?"
                            f"\n• **{prefix}nhie** - Speel Never Have I Ever met de bot.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            help_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            help_embed.set_footer(text=footer)
            await ctx.send(embed=help_embed)
        elif str(ctx.channel) in ecogame_channels:
            help_embed = discord.Embed(
                title="Economie Commands",
                description=f"• **{prefix}with <bedrag>** of **{prefix}with all**"
                            f"\n• **{prefix}dep <bedrag>** of **{prefix}dep all**"
                            f"\n• **{prefix}lb <cash/bank/netto> <pagina>** - Bekijk het hele scorebord."
                            f"\n• **{prefix}bal [naam]** - Bekijk hoeveel geld je hebt."
                            f"\n• **{prefix}reset-economie** - Reset je voortgang naar 0."
                            f"\n• **{prefix}jobs** - Bekijk alle beschikbare jobs."
                            f"\n• **{prefix}job <job>** - Solliciteer voor een job."
                            f"\n• **{prefix}prestige** - Ontgrendel zo meer jobs die je kan kiezen."
                            f"\n• **{prefix}prestige info** - Bekijk meer informatie over prestigen."
                            f"\n• **{prefix}shop <list/koop>** - Koop items uit de shop.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            help_embed.add_field(name="Bedel Command", value=f"__Payout:__ {currency}45 - {currency}100\n__Failrate:__ 5%\n__Cooldown:__ 30 minuten\n__Extra:__ Onbeschikbaar na Prestige 1",
                                 inline=True)
            help_embed.add_field(name="Work Command", value=f"__Payout:__ {currency}80 - {currency}500\n__Failrate:__ 0%\n__Cooldown:__ 1 Uur\n__Extra:__ Moet een job hebben", inline=True)
            help_embed.add_field(name="Slut Command", value=f"__Payout:__ {currency}180 - {currency}380\n__Failrate:__ 20%\n__Cooldown:__ 3 Uur\n__Extra:__ Kleine Kans op Job verliezen", inline=True)
            help_embed.add_field(name="Fish Command", value=f"__Payout:__ {currency}25 - {currency}400\n__Failrate:__ 0%\n__Cooldown:__ 12 Uur\n__Extra:__ Vishengel nodig", inline=True)
            help_embed.add_field(name="Crime Command", value=f"__Payout:__ {currency}850 - {currency}3500\n__Failrate:__ 60%\n__Cooldown:__ 48 Uur\n__Extra:__ Matige Kans op Job verliezen", inline=True)
            help_embed.add_field(name="Rob Command", value=f"__Payout:__ Alle Cash van die speler.\n__Failrate:__ 40%\n__Cooldown:__ 24 Uur\n__Extra:__ Geen", inline=True)
            help_embed.add_field(name="Shop Command (Beperkte Voorraad)", value=f"• **Discord Nitro Classic (1 maand)** - {currency}1.000.000"
                                                                                f"\n• **100MB Bot Hosting (2 maanden)** - {currency}500.000"
                                                                                f"\n• **100MB Bot Hosting (1 maand)** - {currency}330.000"
                                                                                f"\n• **50MB Bot Hosting (2 maanden)** - {currency}270.000"
                                                                                f"\n• **50MB Bot Hosting (1 maand)** - {currency}150.000", inline=False)
            help_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            help_embed.set_footer(text=footer)
            await ctx.send(embed=help_embed)


def setup(client):
    client.add_cog(Commands(client))
