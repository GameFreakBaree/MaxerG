import discord
from discord.ext import commands
import random
from settings import embedcolor, footer, minigame_channels


class NeverHaveIEver(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["nhie", "never-have-i-ever", "ik-heb-nog-nooit", "ikhebnognooit", "ihnn"])
    async def neverhaveiever(self, ctx):
        if str(ctx.channel) in minigame_channels:
            t = ["Ik ben nog nooit in slaap gevallen in de cinema",
                 "Ik heb nog nooit een vals ID gebruikt om ergens binnen te komen",
                 "Ik heb nog nooit iets gewonnen",
                 "Ik ben nog nooit buiten europa op reis geweest",
                 "Ik ben nog nooit geld verloren",
                 "Ik heb nog nooit iets illigaal gedaan",
                 "Ik heb nog nooit mezelf ziekgemeld terwijl ik niet ziek was",
                 "Ik heb nog nooit een foto van mezelf bewerkt",
                 "Ik heb nog nooit een miskoop gedaan",
                 "Ik heb nog nooit iets gestolen",
                 "Ik heb nog nooit geld gegeven aan een zwerver",
                 "Ik ben nog nooit op TV geweest",
                 "Ik heb nog nooit een bericht verstuurd naar de verkeerde persoon",
                 "Ik heb nog nooit iets kapot gemaakt om iets nieuw te krijgen",
                 "Ik heb nog nooit een kledingsstuk andersom gedragen",
                 "Ik heb nog nooit gerookt",
                 "Ik heb nog nooit drugs gebruikt",
                 "Ik heb nog nooit alcohol gedronken",
                 "Ik heb nog nooit een lichaamsdeel gebroken",
                 "Ik heb nog nooit mijn haar geverfd",
                 "Ik heb nog nooit bloed gedoneerd",
                 "Ik ben nog nooit dronken geweest",
                 "Ik heb nog nooit een tattoo gezet",
                 "Ik heb nog nooit iemand zijn wachtwoord gestolen",
                 "Ik heb nog nooit een glas gebroken"]
            responses = random.choice(t)
            embed = discord.Embed(
                description=f"{responses}.\n\n1️⃣ I Have\n2️⃣ I Have Not",
                color=embedcolor
            )
            embed.set_author(name="Never Have I Ever", icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            msg = await ctx.send(embed=embed)
            for emoji in ('1️⃣', '2️⃣'):
                await msg.add_reaction(emoji=f"{emoji}")


def setup(client):
    client.add_cog(NeverHaveIEver(client))
