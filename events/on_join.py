import discord
from discord.ext import commands
import json

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

embed_footer = settings['footer']

read_settings.close()


class OnJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        join_channel = self.client.get_channel(579574134275833869)
        stats_channel = self.client.get_channel(640341412306485251)
        guild_ids = stats_channel.guild

        embed = discord.Embed(
            description=f"Welkom **{member.display_name}** bij **{guild_ids.name}**!",
            color=0x00FF00
        )
        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.set_footer(
            text=f"{embed_footer} | Speler #{guild_ids.member_count}",
            icon_url=self.client.user.avatar_url
        )
        await join_channel.send(embed=embed)

        log_channel = self.client.get_channel(736725990340034591)
        await log_channel.send(f"<:check:725030739543982240> {member} is gejoined!")

        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnJoin(client))
