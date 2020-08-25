import discord
from discord.ext import commands


class OnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        bot_naam = self.client.user.display_name
        print(f"[{bot_naam}] De bot is succesvol geladen.")

        game = discord.Activity(name="Test", type=discord.ActivityType.playing)
        await self.client.change_presence(status=discord.Status.dnd, activity=game)

        stats_channel = self.client.get_channel(742705535899533333)
        guild_ids = stats_channel.guild
        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnReady(client))
