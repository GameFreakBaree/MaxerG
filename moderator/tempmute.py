import discord
import datetime
import json
from discord.ext import commands
import asyncio
from discord.ext.commands import MissingPermissions
from discord.utils import get

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


class Tempmute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, member: discord.Member, duration: int, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author:

            role = get(ctx.guild.roles, name="Muted")
            await member.add_roles(role)

            seconds = duration
            seconds_in_day = 60 * 60 * 24
            seconds_in_hour = 60 * 60
            seconds_in_minute = 60

            days = seconds // seconds_in_day
            hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
            minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute

            premute_embed = discord.Embed(
                description=f"**Reden:** {reason}\n**Duratie:** {days}d {hours}u {minutes}m",
                color=embed_color
            )
            premute_embed.set_author(name=f"{member} is tijdelijk gemute!", icon_url=member.avatar_url)
            await ctx.send(embed=premute_embed)

            log_channel = self.client.get_channel(561243076450975754)
            mute_embed = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            mute_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                 inline=True)
            mute_embed.add_field(name="Moderator", value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}",
                                 inline=True)
            mute_embed.add_field(name="Reden", value=f"{reason}", inline=False)
            mute_embed.add_field(name="Duur", value=f"{days}d {hours}u {minutes}m", inline=False)
            mute_embed.set_author(name=f"[TEMPMUTE] {member}", icon_url=member.avatar_url)
            mute_embed.set_footer(text=embed_footer)
            await log_channel.send(embed=mute_embed)

            await asyncio.sleep(duration)

            role = discord.utils.find(lambda r: r.name == 'Muted', ctx.message.guild.roles)
            if role in member.roles:
                await member.remove_roles(role)

                log_channel = self.client.get_channel(561243076450975754)
                unmute_embed = discord.Embed(
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                unmute_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                       inline=True)
                unmute_embed.add_field(name="Moderator",
                                       value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                unmute_embed.set_author(name=f"[UNMUTE] {member}", icon_url=member.avatar_url)
                unmute_embed.set_footer(text=embed_footer)
                await log_channel.send(embed=unmute_embed)

    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Tempmute(client))
