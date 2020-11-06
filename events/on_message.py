from discord.ext import commands
last_user = 0


class ReactOnMessages(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if f"<@!{self.client.user.id}>" in message.content:
            await message.channel.send(f"De Prefix van deze bot is `!`\nJe kan alle commands zien door `!help`!")

        emoji_channels = ["💡│suggesties"]
        if str(message.channel) in emoji_channels:
            for emoji in ('👍', '👎'):
                await message.add_reaction(emoji=f"{emoji}")

        gtw_channels = ["🐍│woordslang"]
        if str(message.channel) in gtw_channels:
            global last_user
            if last_user == message.author.id:
                await message.delete()
            else:
                last_user = message.author.id

        role_channels = ["🎀│roles"]
        if str(message.channel) in role_channels:
            await message.delete()


def setup(client):
    client.add_cog(ReactOnMessages(client))
