from discord.ext import commands


class OnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        bot_naam = self.client.user.display_name
        print(f"[{bot_naam}] De bot is succesvol geladen.")

        stats_channel = self.client.get_channel(640341412306485251)
        guild_ids = stats_channel.guild
        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnReady(client))
