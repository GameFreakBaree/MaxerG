import asyncio
import datetime
import os
import discord
from discord.ext import commands, tasks
import mysql.connector
from settings import host, user, password, database, token, bot_name, folder_list, embedcolor, footer

client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command("help")


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        status = discord.Activity(name=f"www.MaxerG.net", type=discord.ActivityType.playing)
        await client.change_presence(activity=status)
        await asyncio.sleep(60)


@tasks.loop()
async def check_jobs():
    await client.wait_until_ready()
    await asyncio.sleep(5)
    print(f"\nChecking Jobs at {datetime.datetime.utcnow()}")
    db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
    maxergdb_cursor = db_maxerg.cursor()

    maxergdb_cursor.execute("SELECT * FROM maxerg_economie WHERE job != %s AND job != %s", ("werkloos", "mcdonalds werker"))
    eco_data = maxergdb_cursor.fetchall()
    message = ""
    counter = 0

    for row in eco_data:
        user_id = row[0]
        last_work_time = row[6]
        if last_work_time == "2020-09-25 01:01:01" or last_work_time == "0000-00-00 00:00:00":
            maxergdb_cursor.execute("UPDATE maxerg_economie SET last_work = %s WHERE user_id = %s", (datetime.datetime.utcnow(), user_id))
            db_maxerg.commit()
        else:
            current_time = datetime.datetime.utcnow()
            tijd_ertussen = current_time - last_work_time
            member = await client.fetch_user(user_id)

            if tijd_ertussen.total_seconds() > 86400:
                maxergdb_cursor.execute("UPDATE maxerg_economie SET last_work = %s WHERE user_id = %s", (datetime.datetime.utcnow(), user_id))
                maxergdb_cursor.execute("UPDATE maxerg_economie SET job = %s WHERE user_id = %s", ("werkloos", user_id))
                maxergdb_cursor.execute("UPDATE maxerg_economie SET risico = %s WHERE user_id = %s", (104, user_id))
                db_maxerg.commit()
                counter = 1
                message = f"{message}{member.mention} heeft zijn job verloren..."
    db_maxerg.close()

    if message == "":
        print("0 players lost there jobs.\n")
    else:
        print(f"{counter} players lost there jobs.\n")

        ecogame = client.get_channel(746839771803811902)
        embed = discord.Embed(
            title="Jobs Controle...",
            description=message,
            color=embedcolor
        )
        embed.set_author(name=client.user.display_name, icon_url=client.user.avatar_url)
        embed.set_footer(text=footer)
        await ecogame.send(embed=embed)
    await asyncio.sleep(86395)

for folder in folder_list:
    print(f"[{bot_name}] ----------------------[ {folder.title()} ]--------------------")
    for filename in os.listdir(f'./{folder}'):
        if filename.endswith('.py'):
            print(f"[{bot_name}] {folder.title()} > {filename[:-3]} > Loaded!")
            client.load_extension(f'{folder}.{filename[:-3]}')
print(f"[{bot_name}] ------------------------------------------------------")

client.loop.create_task(change_status())
check_jobs.start()
client.run(token)
