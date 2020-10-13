import discord
from discord.ext import commands
import json
from settings import embedcolor, footer, command_channels


class SmallCmds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['website', 'versie', 'store', 'dynmap'])
    async def ip(self, ctx):
        embed = discord.Embed(
            title="Handige Informatie",
            description="__IP:__ **play.MaxerG.net**\n__Versie:__ **1.12.2 - 1.16.3**\n"
                        "__Website:__ **https://www.maxerg.net/**\n__Shop:__ **https://shop.maxerg.net/**"
                        "\n__Dynmap:__ **https://dynmap.maxerg.net/**",
            color=embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=["users"])
    async def members(self, ctx):
        if str(ctx.channel) in command_channels:
            members_embed = discord.Embed(
                title="Members",
                description=f"Er zijn {ctx.guild.member_count} gebruikers in {ctx.guild.name}!",
                color=embedcolor
            )
            members_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            members_embed.set_footer(text=footer)
            await ctx.send(embed=members_embed)


def setup(client):
    client.add_cog(SmallCmds(client))
