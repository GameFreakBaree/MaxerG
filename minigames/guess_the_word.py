import discord
from discord.ext import commands
import json
import mysql.connector
import asyncio
import random

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()


class HigherLower(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            gtw_channels = ["❓│raad-het-woord"]
            if str(message.channel) in gtw_channels:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
                embed_color_tuple = maxergdb_cursor.fetchone()
                embed_color = int(embed_color_tuple[0], 16)

                maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
                embed_footer = maxergdb_cursor.fetchone()

                maxergdb_cursor.execute("SELECT random_woord FROM maxerg_guessword")
                random_word = maxergdb_cursor.fetchone()

                maxergdb_cursor.execute("SELECT last_user_id FROM maxerg_guessword")
                vorige_id_tuple = maxergdb_cursor.fetchone()
                vorige_id = int(vorige_id_tuple[0])

                if message.author.id == vorige_id:
                    await message.channel.purge(limit=1)
                else:
                    try:
                        update_sql = f"UPDATE maxerg_guessword SET last_user_id = 0"
                        maxergdb_cursor.execute(update_sql)
                        db_maxerg.commit()

                        error_emote = "❌"
                        check_emote = "✅"

                        if message.content.lower() == random_word[0]:
                            await message.add_reaction(emoji=check_emote)

                            embed = discord.Embed(
                                title="Woord Geraden!",
                                description=f"**{message.author.display_name}** heeft het woord geraden!"
                                            f"\n__Woord:__ ` {random_word[0]} `",
                                color=embed_color
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=embed_footer[0])
                            await message.channel.send(embed=embed)

                            t = [
                                "water",
                                "maxerg",
                                "bloemkool",
                                "frieten",
                                "apple",
                                "monitor",
                                "toetsenbord",
                                "muismat",
                                "headset",
                                "papier",
                                "microfoon",
                                "macbook",
                                "iphone",
                                "slaapzak",
                                "boekentas",
                                "rugzak",
                                "gordijn",
                                "airpods",
                                "limonade",
                                "playstation",
                                "simulator",
                                "minecraft",
                                "minetopia",
                                "nachtkastje"
                            ]

                            random_nieuw_woord = random.choice(t)

                            update_sql2 = f"UPDATE maxerg_guessword SET random_woord = %s"
                            maxergdb_cursor.execute(update_sql2, (random_nieuw_woord,))
                            db_maxerg.commit()

                            await asyncio.sleep(3)

                            nieuw_woord_shuffle = list(random_nieuw_woord)
                            random.shuffle(nieuw_woord_shuffle)

                            embed = discord.Embed(
                                title="Raad Het Woord",
                                description=f"Het volgende woord is: ` " + "".join(nieuw_woord_shuffle) + " `",
                                color=embed_color
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=embed_footer[0])
                            await message.channel.send(embed=embed)
                        else:
                            await message.add_reaction(emoji=error_emote)
                    except ValueError:
                        await message.channel.purge(limit=1)
                db_maxerg.close()


def setup(client):
    client.add_cog(HigherLower(client))
