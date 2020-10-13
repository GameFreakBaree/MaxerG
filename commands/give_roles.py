from discord.ext import commands
from discord.utils import get


class CommandsGiveRoles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def role(self, ctx, add_del=None, role=None):
        role_channels = ["🎀│roles"]
        if str(ctx.channel) in role_channels:
            doorgaan = True
            setting = True
            try:
                role = int(role)
                if role is None or add_del is None:
                    doorgaan = False
                elif role == 1:
                    role = "Aankondigingen"
                elif role == 2:
                    role = "Giveaways"
                elif role == 3:
                    role = "MineTopia"
                elif role == 4:
                    role = "Minigames"
                else:
                    doorgaan = False

                if add_del == "add":
                    setting = True
                elif add_del == "remove":
                    setting = False
                else:
                    doorgaan = False

                if doorgaan:
                    giverole = get(ctx.guild.roles, name=role)
                    if ctx.author is not None:
                        if setting:
                            await ctx.author.add_roles(giverole)
                        else:
                            await ctx.author.remove_roles(giverole)
            except ValueError:
                pass

    @commands.Cog.listener()
    async def on_message(self, message):
        role_channels = ["🎀│roles"]
        if str(message.channel) in role_channels:
            await message.delete()


def setup(client):
    client.add_cog(CommandsGiveRoles(client))
