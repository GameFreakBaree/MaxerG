import os
import discord
from discord.ext import commands
import json

with open('db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

token = settings['token']

read_settings.close()

client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command("help")

bot_naam = "MaxerG"


async def change_status():
    await client.wait_until_ready()
    if client.is_ready():
        status = discord.Activity(name=f"www.MaxerG.net", type=discord.ActivityType.playing)
        await client.change_presence(activity=status)


@client.command()
async def load(ctx, types, extension):
    if ctx.author.id == 643072638075273248:
        if extension == "*":
            for filenames in os.listdir(f'./{types}'):
                if filenames.endswith('.py'):
                    print(f"Load {extension}, door {ctx.author}")
                    client.load_extension(f'{types}.{filenames[:-3]}')
            await ctx.send(f"Loaded all extensions in {types}, succes!")
        client.load_extension(f'{types}.{extension}')
        print(f"Load {extension}, door {ctx.author}")
        await ctx.send(f"Load {extension}, succes!")


@client.command()
async def reload(ctx, types, extension):
    if ctx.author.id == 643072638075273248:
        client.unload_extension(f'{types}.{extension}')
        client.load_extension(f'{types}.{extension}')
        print(f"Reload {extension}, door {ctx.author}")
        await ctx.send(f"Reload {extension}, succes!")


@client.command()
async def unload(ctx, types, extension):
    if ctx.author.id == 643072638075273248:
        if extension == "*":
            for filenames in os.listdir(f'./{types}'):
                if filenames.endswith('.py'):
                    print(f"Unload {extension}, door {ctx.author}")
                    client.unload_extension(f'{types}.{filenames[:-3]}')
            await ctx.send(f"Unloaded all extensions in {types}, succes!")
        client.unload_extension(f'{types}.{extension}')
        print(f"Unload {extension}, door {ctx.author}")
        await ctx.send(f"Unload {extension}, succes!")


print(f"[{bot_naam}] ----------------------[ Events ]----------------------")

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        print(f"[{bot_naam}] Events > {filename[:-3]} > Succesvol Geladen!")
        client.load_extension(f'events.{filename[:-3]}')

print(f"[{bot_naam}] ----------------------[ Commands ]--------------------")

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        print(f"[{bot_naam}] Commands > {filename[:-3]} > Succesvol Geladen!")
        client.load_extension(f'commands.{filename[:-3]}')

print(f"[{bot_naam}] ----------------------[ Moderator ]-------------------")

for filename in os.listdir('./moderator'):
    if filename.endswith('.py'):
        print(f"[{bot_naam}] Moderator > {filename[:-3]} > Succesvol Geladen!")
        client.load_extension(f'moderator.{filename[:-3]}')

print(f"[{bot_naam}] ----------------------[ Ecogame ]---------------------")

for filename in os.listdir('./ecogame'):
    if filename.endswith('.py'):
        print(f"[{bot_naam}] Ecogame > {filename[:-3]} > Succesvol Geladen!")
        client.load_extension(f'ecogame.{filename[:-3]}')

print(f"[{bot_naam}] ----------------------[ Minigames ]-------------------")

for filename in os.listdir('./minigames'):
    if filename.endswith('.py'):
        print(f"[{bot_naam}] Minigames > {filename[:-3]} > Succesvol Geladen!")
        client.load_extension(f'minigames.{filename[:-3]}')

client.loop.create_task(change_status())
client.run(token)
