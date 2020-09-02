import discord
from discord.ext import commands
import json

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()
embed_color = int(embedcolor, 16)


class SmallCmds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        verboden_channels = ["✨│hoger-lager"]
        if str(ctx.channel) not in verboden_channels:
            await ctx.send(f"Pong! (Ping: {round(self.client.latency * 1000)}ms)")

    @commands.command(aliases=['website', 'versie', 'shop', 'store', 'dynmap'])
    async def ip(self, ctx):
        verboden_channels = ["✨│hoger-lager"]
        if str(ctx.channel) not in verboden_channels:
            embed = discord.Embed(
                title="Handige Informatie",
                description="__IP:__ **play.MaxerG.net**\n__Versie:__ **1.12.2 - 1.16.1**\n"
                            "__Website:__ **https://www.maxerg.net/**\n__Shop:__ **https://shop.maxerg.net/**"
                            "\n__Dynmap:__ **https://dynmap.maxerg.net/**",
                color=embed_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer)
            await ctx.send(embed=embed)

    @commands.command(aliases=["users"])
    async def members(self, ctx):
        command_channels = ["🤖│commands", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            members_embed = discord.Embed(
                title="Members",
                description=f"Er zijn {ctx.guild.member_count} gebruikers in {ctx.guild.name}!",
                color=embed_color
            )
            members_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            members_embed.set_footer(text=embed_footer)
            await ctx.send(embed=members_embed)


def setup(client):
    client.add_cog(SmallCmds(client))
