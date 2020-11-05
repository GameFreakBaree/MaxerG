import asyncio
import os
import discord
from discord.ext import commands
from settings import token, bot_name, folder_list, prefix

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
client.remove_command("help")
client.actie = "none"


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        status = discord.Activity(name=f"v5-pre6", type=discord.ActivityType.playing)
        await client.change_presence(activity=status)
        await asyncio.sleep(60)

for folder in folder_list:
    print(f"[{bot_name}] ----------------------[ {folder.title()} ]--------------------")
    for filename in os.listdir(f'./{folder}'):
        if filename.endswith('.py'):
            print(f"[{bot_name}] {folder.title()} > {filename[:-3]} > Loaded!")
            client.load_extension(f'{folder}.{filename[:-3]}')
print(f"[{bot_name}] ------------------------------------------------------")


client.loop.create_task(change_status())
client.run(token)
