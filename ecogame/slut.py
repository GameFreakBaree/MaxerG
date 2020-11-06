import discord
from discord.ext import commands
import random
from random import randint
import time
import datetime
import mysql.connector
from settings import host, user, password, database, footer, currency, ecogame_channels, errorcolor


class EcoSlut(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def slut(self, ctx):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            failrate = randint(1, 5)
            if failrate == 3:
                loon = randint(120, 250)
                loon = int(loon)

                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {loon}, netto = netto - {loon} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                mogelijke_antwoorden = [
                    # 0-5
                    f"De politie viel je huis binnen en je kreeg een boete van {currency}{loon}.",
                    f"Een klant viel je aan en heeft {currency}{loon} genomen en is weggelopen.",
                    f"Je bent betrapt toen je een leuke tijd had in de badkamer en kreeg een boete van {currency}{loon}.",
                    f"Je vibrator viel in het midden van je show uit, je klant wou een stuk van zijn geld terug, dus je hebt hem {currency}{loon} betaald.",
                    f"Je was naakt aan het wandelen op de straat en kreeg een boete van {currency}{loon} voor het verstoren van de openbare orde.",
                    # 6-10
                    f"Je bent opgepakt omdat je seks in het openbaar had, je kreeg een boete van {currency}{loon}.",
                    f"Je bent betrapt door in de bib, je betaalt een boete van {currency}{loon}.",
                    f"Je probeerde een sexy standje maar je slipte en brak je been, je betaalde {currency}{loon} aan het ziekenhuis.",
                    f"Terwijl je aan het werken was op de straat voelde je jezelf niet goed. Je ging naar de dokter en hij rekende je {currency}{loon} aan.",
                    f"Je bent betrapt terwijl je seks had in iemand zijn auto en betaalde {currency}{loon} aan de eigenaar van die auto.",
                    # 11-15
                    f"Je gebruikte protectie maar het veroorzaakte een allergische reactie en betaalde {currency}{loon} aan de dokter.",
                    f"Je ging naar beneden bij een boekhouder, de kosten van je belastingen zijn {currency}{loon} verhoogd.",
                    f"Hij wou niet omhoog blijven en je verloor {currency}{loon} aan een klant.",
                    f"Je nam je eigen video op en zette deze op PH. Je baas kwam erachter en je moest {currency}{loon} geven om je job te behouden.",
                    f"Het bed van het hotel hangt vol witte plekken. Je moest {currency}{loon} betalen om het te wassen."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0xFF0000
            else:
                loon = randint(180, 500)
                loon = int(loon)

                maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {loon}, netto = netto + {loon} WHERE user_id = {ctx.author.id}")
                db_maxerg.commit()

                mogelijke_antwoorden = [
                    # 0-5
                    f"Je kreeg {currency}{loon} om te dansen in een stripclub.",
                    f"Je Suger Daddy betaalde je {currency}{loon} voor het werk dat je deed voor hem vorige nacht.",
                    f"Je bent heel goed met je handen en kreeg {currency}{loon}.",
                    f"Je hebt {currency}{loon} verdient om naaktfoto's online te verkopen.",
                    f"Je hebt een Onlyfans gestart en verdiende {currency}{loon} op de eerste dag.",
                    # 5-10
                    f"Je neemt iedereen van het lokale voetbal team. Ze betalen je {currency}{loon}.",
                    f"Je bent goed met deepthroaten en verdiende {currency}{loon} van een klant.",
                    f"Je hebt een leuke nacht en verdiende {currency}{loon}.",
                    f"Je was gisteren dronken en eindigde met een trio, je kan er amper iets van herinneren... maar je hebt er {currency}{loon} aan overgehouden.",
                    f"Je vriend betaalde je {currency}{loon} om zijn voeten te aanbidden."]
                antwoord = random.choice(mogelijke_antwoorden)
                color_succes_fail = 0x1bd115

            em = discord.Embed(
                description=f"{antwoord}",
                color=color_succes_fail,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @slut.error
    async def slut_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 3600:
                conversion = time.strftime("%-Hu %-Mm %-Ss", time.gmtime(error.retry_after))
            else:
                conversion = time.strftime("%-Mm %-Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=errorcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoSlut(client))
