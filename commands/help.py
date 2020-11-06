import discord
from discord.ext import commands
import asyncio
from settings import prefix, currency, embedcolor, footer


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="commands", aliases=["help"])
    async def commands_help(self, ctx):
        help_channels = ["🤖│commands", "💰│economie", "🎨│minigames", "🔒│bots"]
        if str(ctx.channel) in help_channels:
            title_list = ["Algemene Commands", "Ticket Commands", "Fun Commands", "Economie Commands"]
            description_list = [
                f"• **{prefix}help** - Bekijk deze embed!\n• **{prefix}info @<naam>** - Zie info over de getagde speler\n• **{prefix}rank @<naam>** - Zie jouw rank in deze server.\n• **{prefix}levels** - Bekijk het hele level scoreboard.\n• **{prefix}members** - Bekijk hoeveel leden er in {ctx.guild.name} zitten.\n• **{prefix}ping** of **{prefix}uptime** - Bekijk de ping en uptime van de bot.",
                f"• **{prefix}close** - Verwijder je Ticket.\n• **{prefix}add** - Voeg iemand aan je Ticket toe.\n• **{prefix}remove** - Verwijder iemand van je Ticket.",
                f"• **{prefix}rps <steen/papier/schaar>** - Speel Steen Papier Schaar met de bot.\n• **{prefix}wyr** - Krijg een Would You Rather vraag.\n• **{prefix}fact** - Krijg een willekeurig weetje te zien.\n• **{prefix}8ball <vraag>** - Vraag de magische 8ball een vraag.\n• **{prefix}coinflip** - Wordt het kop of munt?\n• **{prefix}nhie** - Speel Never Have I Ever met de bot.",
                f"• **{prefix}regels** - Bekijk de regels van de Economie game.\n• **{prefix}with <bedrag>** of **{prefix}with all**\n• **{prefix}dep <bedrag>** of **{prefix}dep all**\n• **{prefix}lb <cash/bank/netto> <pagina>** - Bekijk het hele scorebord.\n• **{prefix}bal [naam]** - Bekijk hoeveel geld je hebt.\n• **{prefix}reset-economie** - Reset je voortgang naar 0.\n• **{prefix}jobs** - Bekijk alle beschikbare jobs.\n• **{prefix}job <job>** - Solliciteer voor een job.\n• **{prefix}prestige** - Ontgrendel zo meer jobs die je kan kiezen.\n• **{prefix}prestige info** - Bekijk meer informatie over prestigen.\n• **{prefix}shop <list/koop>** - Koop items uit de shop.\n• **{prefix}pay <bedrag> <naam>** - Geef je cash aan iemand anders.\n• **{prefix}team info** - Bekijk alle commands van teams.",
            ]

            pagina = 0
            max_paginas = len(title_list)

            embed = discord.Embed(
                title=title_list[pagina],
                description=description_list[pagina],
                color=embedcolor
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            help_message = await ctx.send(embed=embed)

            await help_message.add_reaction("◀️")
            await help_message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)

                    if str(reaction.emoji) == "▶️" and pagina != max_paginas - 1:
                        pagina += 1
                        new_embed = discord.Embed(
                            title=title_list[pagina],
                            description=description_list[pagina],
                            color=embedcolor
                        )
                        new_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        new_embed.set_footer(text=footer)

                        if pagina == max_paginas - 1:
                            new_embed.add_field(name="Bedel Command", value=f"__Payout:__ {currency}45 - {currency}120\n__Failrate:__ 0%\n__Cooldown:__ 30 Minuten\n__Extra:__ Onbeschikbaar na Prestige 2", inline=True)
                            new_embed.add_field(name="Fish Command", value=f"__Payout:__ {currency}80 - {currency}320\n__Failrate:__ 0%\n__Cooldown:__ 45 Minuten\n__Extra:__ Vishengel nodig", inline=True)
                            new_embed.add_field(name="Work Command", value=f"__Payout:__ {currency}80 - {currency}500\n__Failrate:__ 0%\n__Cooldown:__ 1 Uur\n__Extra:__ Moet een job hebben", inline=True)
                            new_embed.add_field(name="Slut Command", value=f"__Payout:__ {currency}180 - {currency}500\n__Failrate:__ 20%\n__Cooldown:__ 2 Uur", inline=True)
                            new_embed.add_field(name="Crime Command", value=f"__Payout:__ {currency}850 - {currency}4500\n__Failrate:__ 60%\n__Cooldown:__ 24 Uur", inline=True)
                            new_embed.add_field(name="Rob Command", value=f"__Payout:__ 5-50% van de cash.\n__Failrate:__ 40%\n__Cooldown:__ 24 Uur", inline=True)
                            new_embed.add_field(name="Blackjack", value=f"__Gebruik:__ `!bj <bedrag>`\n__Bedrag:__ {currency}100 - {currency}10000\n__Cooldown:__ 4 games per uur", inline=True)
                            new_embed.add_field(name="Roulette", value=f"__Gebruik:__ `!roulette <bedrag> <inzet>`\n__Bedrag:__ {currency}80 - {currency}2000\n__Cooldown:__ 2 games per uur", inline=True)
                            new_embed.add_field(name="Slots", value=f"__Gebruik:__ `!slots <bedrag>`\n__Bedrag:__ {currency}50 - {currency}3000\n__Cooldown:__ 10 games per uur", inline=True)

                        await help_message.edit(embed=new_embed)
                        await help_message.remove_reaction(reaction, user)
                    elif str(reaction.emoji) == "◀️" and pagina > 0:
                        pagina -= 1
                        new_embed = discord.Embed(
                            title=title_list[pagina],
                            description=description_list[pagina],
                            color=embedcolor
                        )
                        new_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        new_embed.set_footer(text=footer)
                        await help_message.edit(embed=new_embed)
                        await help_message.remove_reaction(reaction, user)
                    else:
                        await help_message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    await help_message.clear_reaction("◀️")
                    await help_message.clear_reaction("▶️")
                    break


def setup(client):
    client.add_cog(Commands(client))
