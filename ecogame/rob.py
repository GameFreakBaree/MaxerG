import discord
from discord.ext import commands
import json
import random
from random import randint
import time
import datetime
import mysql.connector

with open('./config.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']
currency = settings['currency']
embedcolor = settings['embedcolor']
embed_footer = settings['footer']
read_settings.close()

embed_color = int(embedcolor, 16)


class EcoRob(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def rob(self, ctx, *, member: discord.Member = None):
        minigame_channels = ["💰│economy-game", "🔒│bots"]
        if str(ctx.channel) in minigame_channels:
            if member is not None:
                if member != ctx.author:
                    db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                    maxergdb_cursor = db_maxerg.cursor()

                    maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_ecogame WHERE user_id = {member.id}")
                    user_id = maxergdb_cursor.fetchone()

                    if user_id is None:
                        instert_new_user_id = "INSERT INTO maxerg_ecogame (user_id, cash, bank) VALUES (%s, %s, %s)"
                        lvl_record = (member.id, 0, 0)
                        maxergdb_cursor.execute(instert_new_user_id, lvl_record)
                        db_maxerg.commit()

                        victem_geld = 0
                    else:
                        maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {member.id}")
                        victem_geld_tuple = maxergdb_cursor.fetchone()
                        victem_geld = victem_geld_tuple[0]

                    if victem_geld <= 0:
                        em = discord.Embed(
                            description=f"<:error:725030739531268187> Deze gebruiker heeft geen geld om te stelen.",
                            color=0xFF0000,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
                        em.set_footer(text=embed_footer[0])
                        await ctx.send(embed=em)
                    else:
                        failrate = randint(0, 1)
                        if failrate == 1:
                            random_loon = randint(120, 280)

                            maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {ctx.author.id}")
                            cash = maxergdb_cursor.fetchone()
                            if cash is None:
                                cash = (0,)

                            loon_cast = cash[0] + random_loon
                            cash_new = 0 - random_loon

                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = {cash_new} WHERE user_id = {ctx.author.id}")
                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto + {cash_new} WHERE user_id = {ctx.author.id}")
                            db_maxerg.commit()

                            mogelijke_antwoorden = [
                                f"Je hebt gestolen van {member.display_name} maar een voorbijganger slog je KO en hij nam {currency}{loon_cast} van je."]
                            antwoord = random.choice(mogelijke_antwoorden)
                            color_succes_fail = 0xFF0000
                        else:
                            maxergdb_cursor.execute(f"SELECT cash FROM maxerg_ecogame WHERE user_id = {member.id}")
                            loon = maxergdb_cursor.fetchone()
                            if loon is None:
                                loon = (0,)

                            loon_cast = loon[0]

                            maxergdb_cursor.execute(f"SELECT bank FROM maxerg_ecogame WHERE user_id = {member.id}")
                            bank = maxergdb_cursor.fetchone()
                            if bank is None:
                                bank = (0,)

                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = 0 WHERE user_id = {member.id}")
                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = {bank} WHERE user_id = {member.id}")
                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET cash = cash + {loon_cast} WHERE user_id = {ctx.author.id}")
                            maxergdb_cursor.execute(f"UPDATE maxerg_ecogame SET netto = netto + {loon_cast} WHERE user_id = {ctx.author.id}")
                            db_maxerg.commit()

                            mogelijke_antwoorden = [
                                f"Je hebt {currency}{loon_cast} gestolen van {member.display_name}."]
                            antwoord = random.choice(mogelijke_antwoorden)
                            color_succes_fail = 0x1bd115

                            await member.send(f'{ctx.author} heeft {currency}{loon_cast} gestolen van je cash!')

                        em = discord.Embed(
                            description=f"{antwoord}",
                            color=color_succes_fail,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        em.set_footer(text=embed_footer)
                        await ctx.send(embed=em)

                    db_maxerg.close()

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 86400:
                conversion = time.strftime("%#dd %#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            elif 3600 <= cooldown_limit < 86400:
                conversion = time.strftime("%#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            else:
                conversion = time.strftime("%#Mm %#Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer)
            await ctx.send(embed=em)
        else:
            raise error


def setup(client):
    client.add_cog(EcoRob(client))
