import discord
from discord.ext import commands
import random
from random import randint
import time
import datetime
import mysql.connector
from settings import host, user, password, database, footer, currency, ecogame_channels, errorcolor


class EcoRob(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def rob(self, ctx, *, member: discord.Member = None):
        if str(ctx.channel) in ecogame_channels:
            if member is not None and member != ctx.author:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_economie WHERE user_id = {member.id}")
                user_id = maxergdb_cursor.fetchone()

                if user_id is None:
                    insert_new_user_id_eco = "INSERT INTO maxerg_economie (user_id, cash, bank, netto, prestige, job, max_bank) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    ecogame_record = (ctx.author.id, 0, 0, 0, 0, "werkloos", 5000)
                    maxergdb_cursor.execute(insert_new_user_id_eco, ecogame_record)
                    db_maxerg.commit()
                    victem_geld = 0
                else:
                    maxergdb_cursor.execute(f"SELECT cash FROM maxerg_economie WHERE user_id = {member.id}")
                    victem_geld_tuple = maxergdb_cursor.fetchone()
                    victem_geld = victem_geld_tuple[0]

                if victem_geld <= 0:
                    em = discord.Embed(
                        description=f"<:error:725030739531268187> Deze gebruiker heeft geen geld om te stelen.",
                        color=0xFF0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
                else:
                    failrate = randint(1, 100)
                    maxergdb_cursor.execute(f"SELECT * FROM maxerg_inventory WHERE user_id = {ctx.author.id}")
                    inventory = maxergdb_cursor.fetchone()
                    slot = inventory[2]
                    geweer = inventory[3]

                    if slot == 1:
                        slot = 10
                    else:
                        slot = 0
                    
                    if geweer == 1:
                        geweer = 20
                    else:
                        geweer = 0

                    percent_bereken = 40 + slot + geweer

                    if failrate <= percent_bereken:
                        random_loon = randint(150, 500)
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {random_loon}, netto = netto - {random_loon} WHERE user_id = {ctx.author.id}")
                        db_maxerg.commit()

                        mogelijke_antwoorden = [
                            f"Je hebt gestolen van {member.display_name} maar een voorbijganger sloeg je KO en hij nam {currency}{random_loon} van je."]
                        antwoord = random.choice(mogelijke_antwoorden)
                        color_succes_fail = 0xFF0000
                    else:
                        maxergdb_cursor.execute(f"SELECT cash FROM maxerg_economie WHERE user_id = {member.id}")
                        cash_member = maxergdb_cursor.fetchone()
                        if cash_member is None:
                            cash_member = (0,)
                        cash_member = cash_member[0]
                        cash_member = cash_member // 2

                        if cash_member <= 102:
                            loon = randint(1, cash_member)
                        else:
                            loon = randint(100, cash_member)

                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash - {loon}, netto = netto - {loon} WHERE user_id = {member.id}")
                        maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {loon}, netto = netto + {loon} WHERE user_id = {ctx.author.id}")
                        db_maxerg.commit()

                        mogelijke_antwoorden = [f"Je hebt {currency}{loon} gestolen van {member.display_name}."]
                        antwoord = random.choice(mogelijke_antwoorden)
                        color_succes_fail = 0x1bd115
                        await member.send(f'{ctx.author} heeft {currency}{loon} gestolen van je cash!')

                    em = discord.Embed(
                        description=f"{antwoord}",
                        color=color_succes_fail,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
                    db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")
            ctx.command.reset_cooldown(ctx)

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 3600:
                conversion = time.strftime("%-Hu %-Mm %-Ss", time.gmtime(error.retry_after))
            else:
                conversion = time.strftime("%-Mm %-Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=errorcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoRob(client))
