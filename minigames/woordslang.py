from discord.ext import commands
import string

last_user = 0
last_word = ""


class Woordslang(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        gtw_channels = ["🐍│woordslang"]
        if str(message.channel) in gtw_channels:
            global last_user
            global last_word

            if last_user == message.author.id:
                await message.delete()
            else:
                bericht = message.content
                bericht = bericht.lower()

                if bericht[-1] in list(string.ascii_lowercase):
                    if last_word == "":
                        last_user = message.author.id
                        last_word = bericht
                    else:
                        if last_word[-1] == bericht[0]:
                            last_user = message.author.id
                            last_word = bericht
                        else:
                            await message.delete()
                else:
                    await message.delete()


def setup(client):
    client.add_cog(Woordslang(client))
