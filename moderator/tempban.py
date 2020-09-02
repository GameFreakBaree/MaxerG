import discord
import datetime
import json
from discord.ext import commands
import asyncio
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


class Tempban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: int = 0, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author and duration != 0:
            seconds = duration
            seconds_in_day = 60 * 60 * 24
            seconds_in_hour = 60 * 60
            seconds_in_minute = 60

            days = seconds // seconds_in_day
            hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
            minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute

            await member.send(f"Je bent tijdelijk verbannen van **{ctx.guild}** door **{ctx.author}** voor **{days}d {hours}u {minutes}m**\n```\nReden: {reason}\n```")

            await member.ban(reason=reason)

            pretempban_embed = discord.Embed(
                description=f"**Reden:** {reason}\n**Duratie:** {days}d {hours}u {minutes}m",
                color=embed_color
            )
            pretempban_embed.set_image(
                url="https://media1.tenor.com/images/de413d89fff5502df7cff9f68b24dca5/tenor.gif?itemid=12850590")
            pretempban_embed.set_author(name=f"{member} is tijdelijk verbannen!", icon_url=member.avatar_url)
            await ctx.send(embed=pretempban_embed)

            log_channel = self.client.get_channel(561243076450975754)
            ban_embed = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            ban_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                inline=True)
            ban_embed.add_field(name="Moderator",
                                value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
            ban_embed.add_field(name="Reden", value=f"{reason}", inline=False)
            ban_embed.add_field(name="Duur", value=f"{days}d {hours}u {minutes}m", inline=False)
            ban_embed.set_author(name=f"[TEMPBAN] {member}", icon_url=member.avatar_url)
            ban_embed.set_footer(text=embed_footer)
            await log_channel.send(embed=ban_embed)

            await asyncio.sleep(duration)

            await ctx.guild.unban(member)

            log_channel = self.client.get_channel(561243076450975754)
            unban_embed = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            unban_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member}",
                                  inline=True)
            unban_embed.add_field(name="Moderator",
                                  value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}",
                                  inline=True)
            unban_embed.set_author(name=f"[UNBAN] {member}", icon_url=ctx.author.default_avatar_url)
            unban_embed.set_footer(text=embed_footer)
            await log_channel.send(embed=unban_embed)

    @tempban.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Tempban(client))
