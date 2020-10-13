import time
import discord
import datetime
from discord.ext import commands
from settings import footer, embedcolor


class Clear(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["purge", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        if amount == 0:
            await ctx.channel.purge(limit=1)
            delete_message = await ctx.send(
                "Je moet een waarde groter dan 0 meegeven aan de command (bv: `!clear 5`).")
            time.sleep(3)
            await delete_message.delete()
        elif amount > 125:
            await ctx.channel.purge(limit=1)
            delete_message = await ctx.send("Je moet een waarde kleiner dan 125 gebruiken.")
            time.sleep(3)
            await delete_message.delete()
        else:
            await ctx.channel.purge(limit=amount + 1)
            if amount == 1:
                delete_message = await ctx.send(f"{amount} bericht is verwijderd!")
                time.sleep(3)
                await delete_message.delete()
            else:
                delete_message = await ctx.send(f"{amount} berichten zijn verwijderd!")
                time.sleep(3)
                await delete_message.delete()

            log_channel = self.client.get_channel(561243076450975754)
            clear_embed = discord.Embed(
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            clear_embed.add_field(name="Moderator", value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}",
                                  inline=True)
            clear_embed.add_field(name="Aantal Berichten", value=f"{amount}", inline=True)
            clear_embed.add_field(name="Channel", value=f"{ctx.channel.mention}", inline=True)
            clear_embed.set_author(name=f"[CLEAR] {ctx.author}", icon_url=ctx.author.avatar_url)
            clear_embed.set_footer(text=footer)
            await log_channel.send(embed=clear_embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass


def setup(client):
    client.add_cog(Clear(client))
