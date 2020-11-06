import discord
from discord.ext import commands
from random import randint
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, currency

min_getal = 1
max_getal = 100000

vorige_id = 0


class HigherLower(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            hl_channels = ["✨│hoger-lager"]
            if str(message.channel) in hl_channels:
                global vorige_id
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute("SELECT random_number FROM maxerg_higherlower")
                luckynumber_tuple = maxergdb_cursor.fetchone()
                luckynumber = int(luckynumber_tuple[0])

                if message.author.id == vorige_id:
                    await message.channel.purge(limit=1)
                else:
                    try:
                        message_inhoud = int(message.content)

                        if message_inhoud > max_getal:
                            await message.channel.purge(limit=1)
                        elif message_inhoud < min_getal:
                            await message.channel.purge(limit=1)
                        else:
                            vorige_id = message.author.id

                            higher_emote = "🔼"
                            lower_emote = "🔽"
                            check_emote = "✅"

                            if message_inhoud > luckynumber:
                                await message.add_reaction(emoji=lower_emote)
                            elif message_inhoud < luckynumber:
                                await message.add_reaction(emoji=higher_emote)
                            elif message_inhoud == luckynumber:
                                await message.add_reaction(emoji=check_emote)

                                random_money = randint(80, 200)

                                embed = discord.Embed(
                                    title="Nummer Geraden!",
                                    description=f"**{message.author.display_name}** heeft het nummer geraden!"
                                                f"\nJe hebt {currency}{random_money} gekregen.",
                                    color=embedcolor
                                )
                                embed.set_footer(text=footer)
                                await message.channel.send(embed=embed)

                                random_number = randint(min_getal, max_getal)

                                maxergdb_cursor.execute(f"UPDATE maxerg_higherlower SET random_number = {random_number}")
                                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash + {random_money} WHERE user_id = {message.author.id}")
                                maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto + {random_money} WHERE user_id = {message.author.id}")
                                db_maxerg.commit()
                    except ValueError:
                        await message.channel.purge(limit=1)
                db_maxerg.close()


def setup(client):
    client.add_cog(HigherLower(client))
