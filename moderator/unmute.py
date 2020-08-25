import discord
import datetime
import json
from discord.ext import commands
import mysql.connector
from discord.ext.commands import MissingPermissions

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


class Unmute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unmute(self, ctx, *, member: discord.Member):
        if member is not None and member != ctx.author:
            db_maxerg.commit()
            maxergdb_cursor = db_maxerg.cursor()

            role = discord.utils.find(lambda r: r.name == 'Muted', ctx.message.guild.roles)
            if role in member.roles:
                await member.remove_roles(role)

                maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
                embed_color_tuple = maxergdb_cursor.fetchone()
                embed_color = int(embed_color_tuple[0], 16)

                preunmute_embed = discord.Embed(
                    color=embed_color
                )
                preunmute_embed.set_author(name=f"{member} is ge-unmute!", icon_url=member.avatar_url)
                await ctx.send(embed=preunmute_embed)

                maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
                embed_footer = maxergdb_cursor.fetchone()

                log_channel = self.client.get_channel(742715965128704030)
                unmute_embed = discord.Embed(
                    color=embed_color,
                    timestamp=datetime.datetime.utcnow()
                )
                unmute_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member.mention}\n**ID:**\t{member.id}",
                                       inline=True)
                unmute_embed.add_field(name="Moderator",
                                       value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}", inline=True)
                unmute_embed.set_author(name=f"[UNMUTE] {member}", icon_url=member.avatar_url)
                unmute_embed.set_footer(text=embed_footer[0])
                await log_channel.send(embed=unmute_embed)
            else:
                await ctx.send(f"{member} is niet gemute.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Unmute(client))
