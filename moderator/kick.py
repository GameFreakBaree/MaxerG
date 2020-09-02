import discord
import datetime
import json
from discord.ext import commands
from discord.ext.commands import MissingPermissions

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']
embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()
embed_color = int(embedcolor, 16)


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author:
            await member.send(f"Je bent gekicked van **{ctx.guild}** door **{ctx.author}**\n```\nReden: {reason}\n```")

            await member.kick(reason=reason)

            prekick_embed = discord.Embed(
                description=f"**Reden:** {reason}",
                color=embed_color
            )
            prekick_embed.set_author(name=f"{member} is gekicked!", icon_url=member.avatar_url)
            await ctx.send(embed=prekick_embed)

            log_channel = self.client.get_channel(561243076450975754)
            kick_embed = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            kick_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                 inline=True)
            kick_embed.add_field(name="Moderator",
                                 value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
            kick_embed.add_field(name="Reden", value=f"{reason}", inline=False)
            kick_embed.set_author(name=f"[KICK] {member}", icon_url=member.avatar_url)
            kick_embed.set_footer(text=embed_footer)
            await log_channel.send(embed=kick_embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Kick(client))
