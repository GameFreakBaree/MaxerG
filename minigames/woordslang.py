from discord.ext import commands
last_user = 0


class WoordSlang(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        gtw_channels = ["🐍│woordslang"]
        if str(message.channel) in gtw_channels:
            global last_user
            if last_user == message.author.id:
                await message.delete()
            else:
                last_user = message.author.id


def setup(client):
    client.add_cog(WoordSlang(client))
