import discord
import datetime
from discord.ext import commands
from settings import footer, embedcolor


class Unban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            unban_user = ban_entry.user

            if (unban_user.name, unban_user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(unban_user)

                preunban_embed = discord.Embed(
                    color=embedcolor
                )
                preunban_embed.set_author(name=f"{member} is niet meer verbannen!", icon_url=ctx.author.default_avatar_url)
                await ctx.send(embed=preunban_embed)

                log_channel = self.client.get_channel(561243076450975754)
                unban_embed = discord.Embed(
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                unban_embed.add_field(name="Gebruiker", value=f"**Naam:**\t{member}",
                                      inline=True)
                unban_embed.add_field(name="Moderator",
                                      value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}",
                                      inline=True)
                unban_embed.set_author(name=f"[UNBAN] {member}", icon_url=ctx.author.default_avatar_url)
                unban_embed.set_footer(text=footer)
                await log_channel.send(embed=unban_embed)
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass


def setup(client):
    client.add_cog(Unban(client))
