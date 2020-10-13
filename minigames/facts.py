from discord.ext import commands
import random
from settings import minigame_channels


class Facts(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["fact", "random-facts", "feit", "feiten"])
    async def facts(self, ctx):
        if str(ctx.channel) in minigame_channels:
            t = ["-89,2 °C de laagste buitentemperatuur ooit gemeten is?",
                 "57,7 °C de hoogste buitentemperatuur ooit gemeten is?", "alleen vrouwelijke muggen steken?",
                 "als je een goudvis in een donkere kamer opsluit, hij wit wordt?",
                 "als je je rechteroog sluit nooit over je rechterschouder kunt kijken?",
                 "Bill Gates in 2010 en 2008 niet de rijkste man is?", "Coca-Cola oorspronkelijk groen was?",
                 "Coca-Cola vroeger cocaïne bevatte?", "dat de meeste vrouwen het vaak kouder hebben dan mannen?",
                 "dat een varken fysiek niet in staat is om naar de lucht te kijken?",
                 "dat net zoals de vingerafdruk ook de tongafdruk bij ieder mens uniek is?",
                 "de aansteker al werd uitgevonden voor de lucifers?",
                 "de aarde ongeveer 6 000 000 000 000 000 000 000 000 kilogram weegt?",
                 "de gemiddelde chauffeur 15.250 keer toeterd in zijn leven?",
                 "de hoogste golf ooit gemeten 64 meter boven de zeespiegel uitkwam?",
                 "de Kolibrie achteruit kan vliegen?",
                 "de langste hartstilstand die iemand overleefde 4 uur duurde?",
                 "de Nijl de langste rivier ter wereld is?",
                 "de omtrek van de aarde wel 40.000 kilometer is?",
                 "de oudste boom ter wereld meer dan 4700 jaar oud is?",
                 "de rijkste man aller tijden John D. Rockefeller is?",
                 "de sterkste spier van het menselijk lichaam de tong is?",
                 "de strepen van een zebra voor verkoeling zorgen?",
                 "de totale lengte van je bloedvaten wel 100.000 kilometer is?",
                 "de zandtijgerhaai zijn broers en zussen op eet voordat hij geboren wordt?",
                 "de zon vlammen uitstoot van 20 tot 50 miljoen graden?", "dieren ook humor hebben?",
                 "dolfijnen en walvissen met één oog open slapen?",
                 "Donald Duck strips verboden waren in Finland, omdat hij geen broek draagt?",
                 "een blinde geen hoogtevrees kan hebben?", "een giraffe net zoveel nekwervels heeft als een mens?",
                 "een kakkerlak 9 dagen in leven kan blijven zonder zijn hoofd?",
                 "een kat meer dan 32 spieren in elk oor heeft?", "een krokodil zijn tong niet kan uitsteken?",
                 "een meerval ruim 27000 smaakpapillen heeft?", "een mens gemiddeld 6000 scheten per jaar laat?",
                 "een slak drie jaar kan slapen?", "een vlo 350 maal zijn lichaamslengte kan springen?",
                 "een vrouw gemiddeld 2 jaar van haar leven in een badkamer doorbengt?",
                 "een worm maar liefst 10 harten heeft?", "een zeester geen hersens heeft?",
                 "er 0,3 procent van de Sahara nodig is om Europa te voorzien van stroom?",
                 "er gemiddeld 100 mensen per jaar stikken in een balpen?",
                 "er niet één normaal Nederlands woord rijmt op het woord twaalf?",
                 "er op zijn minst 9 miljoen mensen jarig zijn op dezelfde dag als jij?",
                 "heet water sneller bevriest dan koud water?", "het absolute nulpunt -273 graden is?",
                 "het bekende spel “Tetris” in 14 dagen is gemaakt?",
                 "het grootste zwembad ter wereld wel 1013 meter lang is?",
                 "het hart bij de mens in het midden van de borstkas zit en niet links?",
                 "het langste woord dat je kunt typen op de linkerhelft van je toetsenbord Verbeteraarsters is?",
                 "het langste woord dat je met de bovenste rij letters kunt maken topprioriteit is?",
                 "het oog van een struisvogel groter is dan zijn hersens?",
                 "het woord ‘van’ de meeste betekenissen heeft?",
                 "ijsberen linkspotig zijn?", "je in de morgen langer bent dan in de avond?",
                 "je niest met een luchtsnelheid van ruim 150 kilometer per uur?", "je niet je ellebogen kunt likken?",
                 "je voet even groot is als de binnenkant van je onderarm?",
                 "meer dan 50 procent van de wereldbevolking nog nooit heeft getelefoneerd?",
                 "mensen die jongleren grotere hersens hebben?", "mensen met rood haar minder pijn voelen?",
                 "Mohammed de meest voorkomende naam is in de wereld?",
                 "olifanten de enige dieren zijn die niet kunnen springen?",
                 "olifanten elkaar vanaf 5 kilometer afstand kunnen ruiken?",
                 "ratten en paarden niet kunnen overgeven?",
                 "rechtshandigen gemiddeld 9 jaar langer leven dan linkshandigen?",
                 "Slechts 20 procent van de Sahara uit zand bestaat?",
                 "te hard niezen kan resulteren in een gebroken rib?",
                 "verdrinking het grootste gevaar is in de woestijn?", "Vlinders met hun poten proeven?",
                 "vrijdag de 17e een ongeluksdag is in Italië?",
                 "vrouwen bijna twee keer zoveel met hun ogen knipperen als mannen?",
                 "de vingerafdruk is bij elk mens uniek, maar ook de tong is uniek bij iedereen. De plaatsing van smaakpapillen, vorm, grootte, etc",
                 "een persoon gedurende zijn leven 25000 liter speeksel produceert.",
                 "een menselijke baby heeft ongeveer 90  botten meer in zijn lichaam dan een volwassen persoon. Een baby wordt geboren met 300 botten, maar als je volwassen wordt, blijven er nog maar 206 over. Dat komt omdat sommige botten in elkaar groeien, zoals in de schedel.",
                 "ons zweet zelf heeft geen enkele geur. De geur is het werk van bacteriën onder je oksels.",
                 "volgens verschillende onderzoeken is iemand met overtollige lichaamsbeharing  veel slimmer dan de gemiddelde mens.",
                 "je oren en neus je hele leven lang blijven groeien",
                 "er op onze planeet ongeveer een miljard verschillende kleuren zijn. Het menselijk oog kan het verschil zien tussen ongeveer 10 miljoen kleuren.",
                 "er meer bacteriën in je mond zitten dan dat er mensen op de wereld zijn",
                 "de hoogste lichaamtemperatuur die men ooit heeft gemeten bij een mens 46,5°C was",
                 "een mens ongeveer 100000km aan bloedvaten heeft, als je deze allemaal achter elkaar zou leggen zou je meer dan 6 keer rond de aarde kunnen gaan.",
                 "maagzuur zelfs metaal kan verteren, dit is niet iets om elke dag te doen want het duurt heel lang vooraleer het verteerd is.",
                 "onze neus echt superslim is? Hij is niet zo goed als bij een hond, maar een mens kan toch gemiddeld tot 50.000 geuren onthouden. Meisjes kunnen ook beter ruiken dan jongens.",
                 "apen, koala's en mensen als enige levende organismen een unieke vingerafdruk hebben",
                 "we 's ochtends langer zijn als in de avond? Dit komt door het kraakbeen in de knie in ons lichaam en de zwaartekracht op aarde.",
                 "de letter \"e\" de meestgebruikte letter is in bijna elke taal die de letter \"e\" bevat."]
            responses = random.choice(t)
            await ctx.send(f"Wist je dat {responses}!")


def setup(client):
    client.add_cog(Facts(client))
