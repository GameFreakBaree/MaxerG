from discord.ext import commands


class OnJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        stats_channel = self.client.get_channel(640341412306485251)
        guild_ids = stats_channel.guild

        log_channel = self.client.get_channel(736725990340034591)
        await log_channel.send(f"<:error:725030739531268187> {member} is geleaved!")

        await stats_channel.edit(name=f"Spelers: {guild_ids.member_count}")


def setup(client):
    client.add_cog(OnJoin(client))
