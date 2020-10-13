from discord.ext import commands


class ReactOnMessages(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if f"<@!{self.client.user.id}>" in message.content:
            await message.channel.send(
                f"De Prefix van deze bot is `!`\nJe kan alle commands zien door `!help`!")

        emoji_channels = ["💡│suggesties"]
        if str(message.channel) in emoji_channels:
            for emoji in ('👍', '👎'):
                await message.add_reaction(emoji=f"{emoji}")

        emoji_channels = ["❓│polls"]
        if str(message.channel) in emoji_channels:
            for emoji in ('1️⃣', '2️⃣', '3️⃣'):
                await message.add_reaction(emoji=f"{emoji}")


def setup(client):
    client.add_cog(ReactOnMessages(client))
