import discord
from discord.ext import commands
import time


class EcoBlackJack(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bj"])
    @commands.cooldown(400, 3600, commands.BucketType.user)
    async def blackjack(self, ctx, inzet=None):
        await ctx.send("Helaas geven we de code hiervan niet vrij.")

    @blackjack.error
    async def blackjack_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
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
    client.add_cog(EcoBlackJack(client))
