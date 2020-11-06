import discord
from discord.ext import commands
from settings import embedcolor, footer, command_channels


class SmallCmds(commands.Cog):

    def __init__(self, client):
        self.client = client

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
