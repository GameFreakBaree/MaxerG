import discord
from discord.ext import commands
import json
from random import randint
import mysql.connector

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


class HigherLower(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            hl_channels = ["✨│hoger-lager"]
            if str(message.channel) in hl_channels:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute("SELECT random_number FROM maxerg_higherlower")
                luckynumber_tuple = maxergdb_cursor.fetchone()
                luckynumber = int(luckynumber_tuple[0])

                maxergdb_cursor.execute("SELECT last_user_id FROM maxerg_higherlower")
                vorige_id_tuple = maxergdb_cursor.fetchone()
                vorige_id = int(vorige_id_tuple[0])

                if message.author.id == vorige_id:
                    await message.channel.purge(limit=1)
                else:
                    try:
                        message_inhoud = int(message.content)

                        maxergdb_cursor.execute(f"UPDATE maxerg_higherlower SET last_user_id = {message.author.id}")
                        db_maxerg.commit()

                        higher_emote = "🔼"
                        lower_emote = "🔽"
                        check_emote = "✅"

                        if message_inhoud > luckynumber:
                            await message.add_reaction(emoji=lower_emote)
                        elif message_inhoud < luckynumber:
                            await message.add_reaction(emoji=higher_emote)
                        elif message_inhoud == luckynumber:
                            await message.add_reaction(emoji=check_emote)

                            random_money = randint(10, 30)

                            embed = discord.Embed(
                                title="Nummer Geraden!",
                                description=f"**{message.author.display_name}** heeft het nummer geraden!"
                                            f"\nJe hebt €{random_money} gekregen.",
                                color=embed_color
                            )
                            embed.set_footer(text=embed_footer)
                            await message.channel.send(embed=embed)

                            random_number = randint(1, 100000)

                            maxergdb_cursor.execute(f"UPDATE maxerg_higherlower SET random_number = {random_number}")
                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash + {random_money} WHERE user_id = {message.author.id}")
                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto + {random_money} WHERE user_id = {message.author.id}")
                            db_maxerg.commit()
                        else:
                            print("error in hoger lager")
                    except ValueError:
                        await message.channel.purge(limit=1)
                db_maxerg.close()


def setup(client):
    client.add_cog(HigherLower(client))
