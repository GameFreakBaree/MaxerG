import discord
import datetime
from discord.ext import commands
from discord.utils import get
from settings import footer, embedcolor


class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author:
            role = get(ctx.guild.roles, name="Muted")
            await member.add_roles(role)

            premute_embed = discord.Embed(
                description=f"**Reden:** {reason}",
                color=embedcolor
            )
            premute_embed.set_author(name=f"{member} is gemute!", icon_url=member.avatar_url)
            await ctx.send(embed=premute_embed)

            log_channel = self.client.get_channel(561243076450975754)
            mute_embed = discord.Embed(
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            mute_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                 inline=True)
            mute_embed.add_field(name="Moderator", value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}",
                                 inline=True)
            mute_embed.add_field(name="Reden", value=f"{reason}", inline=False)
            mute_embed.add_field(name="Duur", value=f"∞", inline=False)
            mute_embed.set_author(name=f"[MUTE] {member}", icon_url=member.avatar_url)
            mute_embed.set_footer(text=footer)
            await log_channel.send(embed=mute_embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass


def setup(client):
    client.add_cog(Mute(client))
