import discord
from discord.ext import commands
import asyncio
from settings import prefix, currency, embedcolor, footer


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="commands", aliases=["help"])
    async def commands_help(self, ctx, *, command=None):
        help_channels = ["🤖│commands", "💰│economie", "🎨│minigames", "🔒│bots"]
        if str(ctx.channel) in help_channels:
            if command is None:
                title_list = ["Algemene Commands", "Ticket Commands", "Fun Commands", "Economie Commands"]
                description_list = [
                    f"• **{prefix}help** - Bekijk deze embed!\n• **{prefix}info @<naam>** - Zie info over de getagde speler\n• **{prefix}rank @<naam>** - Zie jouw rank in deze server.\n• **{prefix}levels** - Bekijk het hele level scoreboard.\n• **{prefix}members** - Bekijk hoeveel leden er in {ctx.guild.name} zitten.\n• **{prefix}ping** of **{prefix}uptime** - Bekijk de ping en uptime van de bot.",
                    f"• **{prefix}close** - Verwijder je Ticket.\n• **{prefix}add** - Voeg iemand aan je Ticket toe.\n• **{prefix}remove** - Verwijder iemand van je Ticket.",
                    f"• **{prefix}rps <steen/papier/schaar>** - Speel Steen Papier Schaar met de bot.\n• **{prefix}wyr** - Krijg een Would You Rather vraag.\n• **{prefix}fact** - Krijg een willekeurig weetje te zien.\n• **{prefix}8ball <vraag>** - Vraag de magische 8ball een vraag.\n• **{prefix}coinflip** - Wordt het kop of munt?\n• **{prefix}nhie** - Speel Never Have I Ever met de bot.",
                    f"• **{prefix}regels** - Bekijk de regels van de Economie game.\n• **{prefix}with <bedrag>** of **{prefix}with all**\n• **{prefix}dep <bedrag>** of **{prefix}dep all**\n• **{prefix}lb [cash/bank/netto/prestige] <pagina>** - Bekijk het hele scorebord.\n• **{prefix}bal [naam]** - Bekijk hoeveel geld je hebt.\n• **{prefix}reset-economie** - Reset je voortgang naar 0.\n• **{prefix}jobs** - Bekijk alle beschikbare jobs.\n• **{prefix}job <job>** - Solliciteer voor een job.\n• **{prefix}prestige** - Ontgrendel zo meer jobs die je kan kiezen.\n• **{prefix}shop [list/koop]** - Koop items uit de shop.\n• **{prefix}pay <bedrag> <naam>** - Geef je cash aan iemand anders.\n• **{prefix}help team** - Bekijk alle commands van teams.\n• **{prefix}daily** - Claim dagelijks je extra beloning.",
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

                def check(reactie, gebruiker):
                    return gebruiker == ctx.author and str(reactie.emoji) in ["◀️", "▶️"]

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
                                new_embed.add_field(name="Bedel Command", value=f"__Payout:__ {currency}20 - {currency}80\n__Failrate:__ 0%\n__Cooldown:__ 30 Minuten\n__Extra:__ Onbeschikbaar na Prestige 2", inline=True)
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
            elif command == "blackjack" or command == "bj":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}blackjack <bedrag>`", inline=False)
                embed.add_field(name="Cooldown:", value="4 games per uur", inline=False)
                embed.add_field(name="Bedrag om in te zetten:", value=f"Minimaal: {currency}100\nMaximaal: {currency}10000", inline=False)
                embed.add_field(name="Uitbetaling:", value=f"**Blackjack betaalt 3 bij 2**\nDus blackjack betaal 1.5x je inzet.", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "roulette":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}roulette <bedrag> <inzet>`", inline=False)
                embed.add_field(name="Voorbeelden:", value=f"`{prefix}roulette 550 zwart`\n`{prefix}roulette 1000 13-24`\n`{prefix}roulette 1800 1st`", inline=False)
                embed.add_field(name="Cooldown:", value="2 games per uur", inline=False)
                embed.add_field(name="Bedrag om in te zetten:", value=f"Minimaal: {currency}80\nMaximaal: {currency}2000", inline=False)
                embed.add_field(name="Uitbetaling Vermenigvuldigers:", value=f"[x30] Nummer (0 t.e.m. 36)\n[x2] Dozijn (1-12, 13-24 of 25-36)\n[x2] Kolom (1st, 2nd of 3rd)\n"
                                                                             f"[x1.5] Manque/Passe (1-18 of 19-36)\n[x1.5] Even/Odd\n[x1.5] Kleur (Rood, Zwart)", inline=False)
                embed.add_field(name="Hoe werken de vermenigvuldigers:", value=f"Stel je gokt op nummer 25 voor {currency}2000 en de bal land op rood 25, dan heb je gewonnen!\n"
                                                                               f"Je uitbetaling is dan 30 * {currency}2000 en is dus {currency}{30 * 2000}", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
                embed.set_image(url="https://i.imgur.com/BotFahm.png")
            elif command == "slots" or command == "slot-machine":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}slots <bedrag>`", inline=False)
                embed.add_field(name="Cooldown:", value="10 games per uur", inline=False)
                embed.add_field(name="Bedrag om in te zetten:", value=f"Minimaal: {currency}50\nMaximaal: {currency}3000", inline=False)
                embed.add_field(name="Uitbetaling Vermenigvuldigers:", value=f"🍎 = 1.5x\n🍍 = 2x\n🍋 = 2.5x\n🍅 = 3x\n🍓 = 3.5x\n🍇 = 4x\n🍒 = 5x", inline=False)
                embed.add_field(name="Hoe werken de vermenigvuldigers:", value=f"Je speelt slots met een bedrag van {currency}2000 en de machine eindigd op 3 keer 🍇, dan win je.\n"
                                                                               f"Je uitbetaling is dan 4 * {currency}2000 en is dus {currency}{4 * 2000}", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "prestige":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}prestige`", inline=False)
                embed.add_field(name="Wat Is Prestigen:", value="Dankzij prestigen kan je hogere jobs ontgrendelen. Bij elke prestige krijg je meer opslag in je bank.", inline=False)
                embed.add_field(name="Voordelen:", value=f"\n• __Prestige 0 (standaard)__ ─ __Prijs:__ {currency}0 ─ Bank Opslag: {currency}5.000, Jobs: 1\n• __Prestige 1__ ─ __Prijs:__ {currency}8.000 ─ Opslag: {currency}10.000, Jobs: 2"
                                                         f"\n• __Prestige 2__ ─ __Prijs:__ {currency}12.000 ─ Opslag: {currency}20.000, Jobs: 3\n• __Prestige 3__ ─ __Prijs:__ {currency}18.000 ─ Opslag: {currency}35.000, Jobs: 4"
                                                         f"\n• __Prestige 4__ ─ __Prijs:__ {currency}26.000 ─ Opslag: {currency}60.000, Jobs: 5\n• __Prestige 5__ ─ __Prijs:__ {currency}35.000 ─ Opslag: {currency}80.000, Jobs: 6"
                                                         f"\n• __Prestige 6__ ─ __Prijs:__ {currency}48.000 ─ Opslag: {currency}130.000, Jobs: 7\n• __Prestige 7__ ─ __Prijs:__ {currency}60.000 ─ Opslag: {currency}175.000, Jobs: 8"
                                                         f"\n• __Prestige 8__ ─ __Prijs:__ {currency}72.000 ─ Opslag: {currency}250.000, Jobs: 9\n• __Prestige 9__ ─ __Prijs:__ {currency}90.000 ─ Opslag: {currency}300.000, Jobs: 10"
                                                         f"\n• __Prestige 10__ ─ __Prijs:__ {currency}100.000 ─ Opslag: {currency}360.000, Jobs: 11\n• __Prestige 11__ ─ __Prijs:__ {currency}112.000 ─ Opslag: {currency}420.000, Jobs: 12"
                                                         f"\n• __Prestige 12__ ─ __Prijs:__ {currency}125.000 ─ Opslag: {currency}500.000, Jobs: 13", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "work":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Deze command wordt gebruikt om te werken om zo extra geld te verdienen.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}work`", inline=False)
                embed.add_field(name="Cooldown:", value="1 uur", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}50\nMaximaal: {currency}850", inline=False)
                embed.add_field(name="Extra:", value=f"Je moet een job hebben om gebruik te maken van deze command\nDoe `{prefix}help job` om hierover meer te weten.", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "slut":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="-- Waarschuwing --", value="Deze command kan NSFW items bevatten. Gebruiken op eigen risico.", inline=False)
                embed.add_field(name="Beschrijving:", value="Laat de seksuele kant van je zien om zo geld te verdienen.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}slut`", inline=False)
                embed.add_field(name="Cooldown:", value="2 uur", inline=False)
                embed.add_field(name="Failrate:", value="20% kans om te falen", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}180\nMaximaal: {currency}500", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "crime":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Steel spullen om zo rijker te worden.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}crime`", inline=False)
                embed.add_field(name="Cooldown:", value="24 uur", inline=False)
                embed.add_field(name="Failrate:", value="60% kans om te falen", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}850\nMaximaal: {currency}4500", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "rob":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Steel cash van een andere speler.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}rob <naam>`", inline=False)
                embed.add_field(name="Cooldown:", value="12 uur", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}5% van de cash van de speler\nMaximaal: {currency}50% van de cash van de speler", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "with" or command == "withdraw" or command == "dep" or command == "deposit":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Zet geld van je cash op je bank. (Deposit | Dep)\nOf haal geld van je bank af. (Withdraw | With)", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}{command.lower()} <bedrag | all>`", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "team" or command == "teams":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value=f"Dankzij een team kan je leden in je team geld sturen.\nWil je meer weten over andere mensen geld sturen? Doe dan `{prefix}help pay`", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}team <optie> [naam]`", inline=False)
                embed.add_field(name="Commands:", value=f"`{prefix}team maak` - Maak een team aan.\n`{prefix}team verwijder` - Verwijder je team."
                                                        f"\n`{prefix}team verlaat` - Verlaat je team.\n`{prefix}team remove <naam>` - Verwijder iemand van je team."
                                                        f"\n`{prefix}team invite <naam>` - Invite iemand naar je team.\n`{prefix}team list` - Bekijk wie er allemaal in je team zit.", inline=False)
                embed.add_field(name="Maximale Team grootte:", value=f"3 in totaal. (2 leden, 1 leider)", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "inventory" or command == "inv":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value=f"Bekijk alle items dat je gekocht hebt in de shop.\nWil je meer info weten over de shop? Doe dan `{prefix}shop`.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}inventory`", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "fish":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Ga vissen, en verkoop de vissen om zo extra geld te verdienen.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}fish`", inline=False)
                embed.add_field(name="Cooldown:", value="45 minuten", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}80\nMaximaal: {currency}320", inline=False)
                embed.add_field(name="Extra:", value=f"Je moet een vishengel hebben om te vissen.\nDoe `{prefix}help shop` om hierover meer te weten.", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "daily":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Claim je dagelijks geld en word elke dag rijker.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}daily`", inline=False)
                embed.add_field(name="Cooldown:", value="24 uur", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}80\nMaximaal: {currency}320", inline=False)
                embed.add_field(name="Extra:", value=f"Je moet een bepaald level zijn om deze command te gebruiken.\nDoe `{prefix}help leveling` om hierover meer te weten.\nBekijk ook zeker <#714116295175438457> voor meer info.", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "balance" or command == "bal":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Bekijk hoeveel geld je hebt in cash en bank.\nJe kan hiermee ook je netto bekijken en je maximale geld op de bank.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}{command.lower()} [naam]`", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "hoger lager" or command == "hoger" or command == "lager" or command == "higher lower" or command == "hoger-lager" or command == "higher-lower":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Raad een getal en de bot zegt alleen of het winnende getal hoger of lager is.", inline=False)
                embed.add_field(name="Cooldown:", value="Totdat een andere speler iets stuurt in die channel.", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}80\nMaximaal: {currency}200", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#738804088111759361>", inline=False)
            elif command == "gtw" or command == "guess the word" or command == "raad het woord" or command == "raad-het-woord" or command == "raadhetwoord" or command == "rhw" or command == "woord raden":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Je krijgt een woord met alle letters door mekaar. Het is jouw taak om het woord te raden.", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}20\nMaximaal: {currency}80", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#747190227097092267>", inline=False)
            elif command == "leveling":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Krijg geld en xp om te typen in discord.", inline=False)
                embed.add_field(name="Gebruik Commands:", value=f"`{prefix}rank [naam]`\n`{prefix}levels`", inline=False)
                embed.add_field(name="Cooldown:", value=f"30 seconden", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"Elke channel van de discord server.", inline=False)
            elif command == "pay":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Geef jouw cash aan iemand anders van je team.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}pay <bedrag> <naam>`", inline=False)
                embed.add_field(name="Extra:", value=f"Je moet in een team zitten om deze command te kunnen gebruiken.\nDoe `{prefix}help team` om hierover meer te weten.", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "ticket" or command == "tickets":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Een ticket maakt een channel waar alleen jij inkan en de staffleden van MaxerG.", inline=False)
                embed.add_field(name="Ticket aanmaken:", value=f"Klik de gepaste emote aan in <#726058921881763911>.", inline=False)
                embed.add_field(name="Gebruik Commands:", value=f"`{prefix}ticket close`\n`{prefix}ticket add <naam>`\n`{prefix}ticket remove <naam>`", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"Ticket aanmaken in: <#726058921881763911>\nTicket commands in: jouw ticket channel.", inline=False)
            elif command == "woordslang" or command == "wordsnake":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Maak 1 lange zin met maar 1 woord per bericht.", inline=False)
                embed.add_field(name="Cooldown:", value="Totdat een andere speler iets stuurt in die channel.", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#763361275631239200>", inline=False)
            elif command == "job" or command == "jobs":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value=f"Dankzij deze command kan je `{prefix}work` doen en daarmee geld verdienen.", inline=False)
                embed.add_field(name="Gebruik Commands:", value=f"`{prefix}jobs` - krijg een lijst van alle beschikbare jobs.\n`{prefix}job <job naam>` - Solliciteer voor de job.", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}45\nMaximaal: {currency}120", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            elif command == "bedel":
                embed = discord.Embed(
                    title=f"Help: {command.title()}",
                    color=embedcolor
                )
                embed.add_field(name="Beschrijving:", value="Deze command wordt gebruikt om te bedelen voor geld.", inline=False)
                embed.add_field(name="Gebruik Command:", value=f"`{prefix}bedel`", inline=False)
                embed.add_field(name="Cooldown:", value="30 minuten", inline=False)
                embed.add_field(name="Geld te verdienen:", value=f"Minimaal: {currency}20\nMaximaal: {currency}80", inline=False)
                embed.add_field(name="Te gebruiken in:", value=f"<#708055327958106164>", inline=False)
            else:
                embed = discord.Embed(
                    title="Beschikbare Help Commands",
                    description=f"**Algemeen**\n"
                                f"`leveling`, `ticket`"
                                f"\n\n**Minigames**\n"
                                f"`hoger lager`, `raad het woord`, `woordslang`"
                                f"\n\n**Economie**\n"
                                f"`bedel`, `work`, `slut`, `crime`, `fish`, `inventory`, `team`, `pay`, `withdraw`, `deposit`, `rob`, `daily`, `prestige`, `job`"
                                f"\n\n**Casino Games**\n"
                                f"`blackjack`, `roulette`, `slots`"
                                f"\n\n**Voorbeelden:** `{prefix}help work`, `{prefix}help raad het woord` of `{prefix}help ticket`",
                    color=embedcolor
                )

            if command is not None:
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
