from discord.ext import commands
import random
import time


class EightBall(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question=None):
        command_channels = ["🎨│minigames", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            if question is None:
                await ctx.send("Waar heb je 8ball nodig voor?")
            else:
                t = ["Het is zeker", "Reactie is wazig, probeer opnieuw", "Het is beslist zo", "Vraag later opnieuw",
                     "Zonder twijfel", "Beter je nu niet te zeggen", "Zeer zeker", "Niet nu te voorspellen",
                     "Je kunt erop vertrouwen", "Concentreer je en vraag opnieuw", "Volgens mij wel",
                     "Reken er niet op",
                     "Zeer waarschijnlijk", "Mijn antwoord is nee", "Goed vooruitzicht", "Mijn bronnen zeggen nee",
                     "Ja",
                     "Vooruitzicht is niet zo goed", "Tekenen wijzen op ja", "Zeer twijfelachtig"]
                responses = random.choice(t)
                await ctx.send(responses)
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#721013671307772587> zitten om deze command uit te voeren.")
            time.sleep(3)
            await del_msg.delete()


def setup(client):
    client.add_cog(EightBall(client))
