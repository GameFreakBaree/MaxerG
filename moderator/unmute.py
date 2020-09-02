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


class Unmute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def unmute(self, ctx, *, member: discord.Member):
        if member is not None and member != ctx.author:
            role = discord.utils.find(lambda r: r.name == 'Muted', ctx.message.guild.roles)
            if role in member.roles:
                await member.remove_roles(role)

                preunmute_embed = discord.Embed(
                    color=embed_color
                )
                preunmute_embed.set_author(name=f"{member} is ge-unmute!", icon_url=member.avatar_url)
                await ctx.send(embed=preunmute_embed)

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
            else:
                await ctx.send(f"{member} is niet gemute.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Unmute(client))
