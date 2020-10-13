import discord
import datetime
from discord.ext import commands
from settings import footer, embedcolor


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author:
            await member.send(f"Je bent verbannen van **{ctx.guild}** door **{ctx.author}**\n```\nReden: {reason}\n```")

            await member.ban(reason=reason)

            preban_embed = discord.Embed(
                description=f"**Reden:** {reason}",
                color=embedcolor
            )
            preban_embed.set_image(url="https://media1.tenor.com/images/de413d89fff5502df7cff9f68b24dca5/tenor.gif?itemid=12850590")
            preban_embed.set_author(name=f"{member} is verbannen!", icon_url=member.avatar_url)
            await ctx.send(embed=preban_embed)

            log_channel = self.client.get_channel(561243076450975754)
            ban_embed = discord.Embed(
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            ban_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                inline=True)
            ban_embed.add_field(name="Moderator",
                                value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
            ban_embed.add_field(name="Reden", value=f"{reason}", inline=False)
            ban_embed.add_field(name="Duur", value=f"∞", inline=False)
            ban_embed.set_author(name=f"[BAN] {member}", icon_url=member.avatar_url)
            ban_embed.set_footer(text=footer)
            await log_channel.send(embed=ban_embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass


def setup(client):
    client.add_cog(Ban(client))
