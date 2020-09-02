import discord
import datetime
import time
import json
from discord.ext import commands

start_time = time.time()

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']
embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()
embed_color = int(embedcolor, 16)


class Uptime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def uptime(self, ctx):
        command_channels = ["🤖│commands", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))

            embed = discord.Embed(
                title="Uptime",
                description=f"{text}",
                color=embed_color
            )
            embed.set_footer(text=embed_footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Uptime(client))
