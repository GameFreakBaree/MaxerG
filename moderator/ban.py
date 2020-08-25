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


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="Niet Vermeld"):
        if member is not None and member != ctx.author:
            db_maxerg.commit()
            maxergdb_cursor = db_maxerg.cursor()

            await member.send(f"Je bent verbannen van **{ctx.guild}** door **{ctx.author}**\n```\nReden: {reason}\n```")

            await member.ban(reason=reason)

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            preban_embed = discord.Embed(
                description=f"**Reden:** {reason}",
                color=embed_color
            )
            preban_embed.set_image(url="https://media1.tenor.com/images/de413d89fff5502df7cff9f68b24dca5/tenor.gif?itemid=12850590")
            preban_embed.set_author(name=f"{member} is verbannen!", icon_url=member.avatar_url)
            await ctx.send(embed=preban_embed)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            log_channel = self.client.get_channel(742715965128704030)
            ban_embed = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            ban_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                inline=True)
            ban_embed.add_field(name="Moderator",
                                value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
            ban_embed.add_field(name="Reden", value=f"{reason}", inline=False)
            ban_embed.add_field(name="Duur", value=f"∞", inline=False)
            ban_embed.set_author(name=f"[BAN] {member}", icon_url=member.avatar_url)
            ban_embed.set_footer(text=embed_footer[0])
            await log_channel.send(embed=ban_embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Ban(client))
