import discord
from discord.ext import commands
import mysql.connector
import asyncio
import random
from settings import host, user, password, database, embedcolor, footer

t = ["EMPTY"]


class GuessTheWord(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            gtw_channels = ["❓│raad-het-woord"]
            if str(message.channel) in gtw_channels:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute("SELECT * FROM maxerg_guessword")
                gtw_data = maxergdb_cursor.fetchone()
                random_word = gtw_data[0]
                votes = gtw_data[1]
                vote1 = gtw_data[2]
                vote2 = gtw_data[3]
                vote_list = [vote1, vote2]

                error_emote = "❌"
                check_emote = "✅"

                if message.content.lower() == random_word:
                    await message.add_reaction(emoji=check_emote)

                    embed = discord.Embed(
                        title="Woord Geraden!",
                        description=f"**{message.author.display_name}** heeft het woord geraden!"
                                    f"\n__Woord:__ ` {random_word} `",
                        color=embedcolor
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await message.channel.send(embed=embed)

                    random_nieuw_woord = random.choice(t)
                    maxergdb_cursor.execute("UPDATE maxerg_guessword SET random_woord = %s", [random_nieuw_woord])
                    maxergdb_cursor.execute("UPDATE maxerg_guessword SET votes = 0")
                    maxergdb_cursor.execute("UPDATE maxerg_guessword SET vote_one = 0")
                    maxergdb_cursor.execute("UPDATE maxerg_guessword SET vote_two = 0")
                    db_maxerg.commit()

                    async with message.channel.typing():
                        await asyncio.sleep(3)

                    nieuw_woord_shuffle = list(random_nieuw_woord)
                    random.shuffle(nieuw_woord_shuffle)

                    embed = discord.Embed(
                        title="Raad Het Woord",
                        description=f"Het volgende woord is: ` " + "".join(nieuw_woord_shuffle) + " `",
                        color=embedcolor
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=f"{footer} | Type '?' om dit woord over te slaan.")
                    await message.channel.send(embed=embed)
                elif message.content.lower() == "?":
                    if votes == 2:
                        if message.author.id not in vote_list:
                            embed = discord.Embed(
                                title="Woord Gereset!",
                                description=f"**Niemand** heeft het woord geraden!"
                                            f"\n__Woord:__ ` {random_word} `",
                                color=embedcolor
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer}")
                            await message.channel.send(embed=embed)

                            random_nieuw_woord = random.choice(t)
                            maxergdb_cursor.execute("UPDATE maxerg_guessword SET random_woord = %s", [random_nieuw_woord])
                            maxergdb_cursor.execute("UPDATE maxerg_guessword SET votes = 0")
                            maxergdb_cursor.execute("UPDATE maxerg_guessword SET vote_one = 0")
                            maxergdb_cursor.execute("UPDATE maxerg_guessword SET vote_two = 0")
                            db_maxerg.commit()

                            async with message.channel.typing():
                                await asyncio.sleep(3)

                            nieuw_woord_shuffle = list(random_nieuw_woord)
                            random.shuffle(nieuw_woord_shuffle)

                            embed = discord.Embed(
                                title="Raad Het Woord",
                                description=f"Het volgende woord is: ` " + "".join(nieuw_woord_shuffle) + " `",
                                color=embedcolor
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer} | Type '?' om dit woord over te slaan.")
                            await message.channel.send(embed=embed)
                    else:
                        if message.author.id not in vote_list:
                            if 2-votes == 1:
                                woord = "vote"
                            else:
                                woord = "votes"

                            embed = discord.Embed(
                                title="Raad Het Woord",
                                description=f"Bedankt voor het voten! Nog {2 - votes} {woord} nodig.",
                                color=embedcolor
                            )
                            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                            embed.set_footer(text=f"{footer} | Type '?' om dit woord over te slaan.")
                            await message.channel.send(embed=embed)

                            if votes+1 == 1:
                                maxergdb_cursor.execute(f"UPDATE maxerg_guessword SET vote_one = {message.author.id}")
                            elif votes+1 == 2:
                                maxergdb_cursor.execute(f"UPDATE maxerg_guessword SET vote_two = {message.author.id}")

                            maxergdb_cursor.execute("UPDATE maxerg_guessword SET votes = votes + 1")
                            db_maxerg.commit()
                else:
                    await message.add_reaction(emoji=error_emote)
                db_maxerg.close()


def setup(client):
    client.add_cog(GuessTheWord(client))
