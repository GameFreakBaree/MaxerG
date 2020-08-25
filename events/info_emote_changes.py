import discord
from discord.ext import commands


class OnEmoteChange(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        if message_id == 714121760064143422:
            role = None
            if payload.emoji.name == "📢":
                role = discord.utils.get(guild.roles, name="Aankondigingen")
            elif payload.emoji.name == "minecraft":
                role = discord.utils.get(guild.roles, name="MineTopia")
            elif payload.emoji.name == "📌":
                role = discord.utils.get(guild.roles, name="Polls")
            elif payload.emoji.name == "🖼️":
                role = discord.utils.get(guild.roles, name="Sneakpeeks")
            elif payload.emoji.name == "💰":
                role = discord.utils.get(guild.roles, name="Minigames")

            if role is not None:
                if member is not None:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 714121760064143422:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

            role = None
            if payload.emoji.name == "📢":
                role = discord.utils.get(guild.roles, name="Aankondigingen")
            elif payload.emoji.name == "minecraft":
                role = discord.utils.get(guild.roles, name="MineTopia")
            elif payload.emoji.name == "📌":
                role = discord.utils.get(guild.roles, name="Polls")
            elif payload.emoji.name == "🖼️":
                role = discord.utils.get(guild.roles, name="Sneakpeeks")
            elif payload.emoji.name == "💰":
                role = discord.utils.get(guild.roles, name="Minigames")

            if role is not None:
                if member is not None:
                    await member.remove_roles(role)


def setup(client):
    client.add_cog(OnEmoteChange(client))
