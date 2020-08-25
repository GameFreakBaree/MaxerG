import discord
import datetime
import json
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()

db_maxerg = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    passwd=password
)


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author:
            db_maxerg.commit()
            maxergdb_cursor = db_maxerg.cursor()

            await member.send(f"Je bent gekicked van **{ctx.guild}** door **{ctx.author}**\n```\nReden: {reason}\n```")

            await member.kick(reason=reason)

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            prekick_embed = discord.Embed(
                description=f"**Reden:** {reason}",
                color=embed_color
            )
            prekick_embed.set_author(name=f"{member} is gekicked!", icon_url=member.avatar_url)
            await ctx.send(embed=prekick_embed)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            log_channel = self.client.get_channel(742715965128704030)
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
            kick_embed.set_footer(text=embed_footer[0])
            await log_channel.send(embed=kick_embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Kick(client))
