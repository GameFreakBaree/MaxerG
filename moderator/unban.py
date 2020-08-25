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


class Unban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        db_maxerg.commit()
        maxergdb_cursor = db_maxerg.cursor()

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
        embed_color_tuple = maxergdb_cursor.fetchone()
        embed_color = int(embed_color_tuple[0], 16)

        maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
        embed_footer = maxergdb_cursor.fetchone()

        for ban_entry in banned_users:
            unban_user = ban_entry.user

            if (unban_user.name, unban_user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(unban_user)

                preunban_embed = discord.Embed(
                    color=embed_color
                )
                preunban_embed.set_author(name=f"{member} is niet meer verbannen!", icon_url=ctx.author.default_avatar_url)
                await ctx.send(embed=preunban_embed)

                log_channel = self.client.get_channel(742715965128704030)
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
                unban_embed.set_footer(text=embed_footer[0])
                await log_channel.send(embed=unban_embed)
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Unban(client))
