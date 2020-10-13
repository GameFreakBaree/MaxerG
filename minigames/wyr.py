from discord.ext import commands
import random
from settings import minigame_channels


class WouldYouRather(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["would-you-rather", "wouldyourather", "wil-je-liever", "wiljeliever", "wjl"])
    async def wyr(self, ctx):
        if str(ctx.channel) in minigame_channels:
            t = ["de slimste persoon in een groep mensen zijn of de knapste?",
                 "doorgaan met je huidige leven of opnieuw beginnen als dat mogelijk was?", "doof zijn of blind?",
                 "behaard willen zijn of helemaal zonder haren?",
                 "altijd 10 minuten te laat zijn of 20 minuten te vroeg?",
                 "al je foto’s kwijtraken of al je geld?", "knap en dom willen zijn of intelligent maar lelijk?",
                 "door iedereen gevreesd worden of geliefd zijn door iedereen?",
                 "de liefde van je leven ontmoeten of drie miljoen euro vinden?",
                 "nooit geen vlees meer eten of groenten?",
                 "geen kinderen krijgen of alleen drielingen?", "rijst bij elke maaltijd eten of brood?",
                 "5cm groter of 5cm kleiner willen zijn?", "iets te laat zijn of veel te vroeg?",
                 "alleen werken of met een groep mensen?", "teveel overgewicht of ondergewicht hebben?",
                 "meer tijd willen of meer geld?", "jezelf blijven of iemand anders (als dat kon)?",
                 "te druk zijn of verveeld?", "kaal zijn of altijd een slechte kapbeurt meemaken?",
                 "een maand zonder internet zitten of een maand niet douchen?",
                 "gratis Wifi hebben in de trein of gratis koffie?",
                 "als zwerver in de stad willen leven of ver van de mensen in de natuur?",
                 "stoppen met social media apps of televisie kijken?", "sneller kunnen typen of sneller kunnen lezen?",
                 "een zelfrijdende auto willen of een volledig geautomatiseerd huis?",
                 "nooit je sleutels kwijtraken of je smartphone?", "aan het strand wonen of in een huis in de bossen?",
                 "zonder je linkerhand verder moeten of je rechtervoet?",
                 "alleen maar scherp gekruid eten of alleen maar smaakloos eten?",
                 "zelf een huis ontwerpen en bouwen of het door een architect en aannemer laten doen?",
                 "de badkamer poetsen of de vaat wassen?",
                 "de beste speler van het veld zijn maar toch verliezen of winnen terwijl je op de bank zit?",
                 "voor een groep mensen die je kent zingen of voor een groep onbekende personen?",
                 "twee weken gaan backpacken in Azië of lig je liever in twee weken aan het strand in Spanje?",
                 "geld willen voor je verjaardag of een cadeau?",
                 "in een klein huis in een goede buurt wonen of een riant huis in een slechte buurt?",
                 "parachutespringen of bungee jumpen?", "buiten werken of een kantoorbaan hebben?",
                 "het goede of het slechte nieuws eerst horen?", "voor jezelf werken of voor een baas?",
                 "stelen of vreemdgaan?",
                 "meer uren per dag maar minder dagen per week willen werken of meer dagen per week en minder uren per dag?",
                 "een nacht in een luxueus hotel doorbrengen of in een tent met mooi uitzicht?",
                 "in een land wonen waar het altijd koud is of in een zomers land?",
                 "één beste vriend(in) hebben of vele goede kennissen?",
                 "de hele dag op een huilend kind passen of een week lang een zeurende schoonmoeder op bezoek hebben?",
                 "opgesloten zijn in een bibliotheek of in een avonturenpark?",
                 "ten huwelijk gevraagd worden met veel publiek erbij of tijdens een intiem onderonsje?",
                 "in een grot wonen of een boomhuis?", "een kok in huis willen of een schoonmaakster?",
                 "geen bezoekers op je bruiloft willen of op je begrafenis?", "nooit meer zweten of het koud hebben?",
                 "een koe zijn of een kip?", "echte liefde vinden of 1 miljoen euro?",
                 "een jacht willen hebben of een vliegtuig?", "meer geld willen of meer tijd?",
                 "Batman of Spiderman zijn?",
                 "2 keer zo klein of 2 keer zo zwaar willen zijn?", "jezelf blijven of iemand anders worden?",
                 "de slimste persoon willen zijn of de knapste?", "kunnen vliegen of gedachten lezen?",
                 "doof zijn of blind?", "een stand-up comedian zijn of een pianist?",
                 "altijd weten dat iemand liegt of zelfs nooit betrapt worden op liegen?",
                 "een advocaat of een dokter willen zijn?",
                 "je voorouders willen ontmoeten of je toekomstige volwassen kleinkinderen?",
                 "het begin van de aarde willen meemaken of het einde?",
                 "alle talen spreken of met dieren kunnen praten?",
                 "altijd willen weten als iemand liegt of zelf kunnen liegen en niemand het door heeft?",
                 "voor een dag kunnen vliegen of onzichtbaar zijn?",
                 "een jaar lang dezelfde dag herleven of een jaar verliezen?",
                 "een succesvolle acteur willen zijn of regisseur?",
                 "alleen op een onbewoond eiland zitten of samen met iemand die niet kan ophouden met praten?",
                 "het nieuws presenteren of meedoen aan een realityshow?",
                 "een Nobel prijs winnen of een Olympische medaille?",
                 "vier kinderen willen en geen geld of geen kinderen en vier miljoen euro?",
                 "willen weten wanneer je dood gaat of hoe je dood gaat?",
                 "nooit meer in de file staan of nooit meer struikelen in het openbaar?"]
            responses = random.choice(t)
            msg = await ctx.send(f"Wil je liever {responses}!")
            for emoji in ('1️⃣', '2️⃣'):
                await msg.add_reaction(emoji=f"{emoji}")


def setup(client):
    client.add_cog(WouldYouRather(client))
