import discord
from discord.ext import commands
from random import randint
from discord.utils import get
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, command_channels
import asyncio


class LevelingSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is False:
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                pass
            else:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()
                random_exp = randint(3, 7)

                maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_levels WHERE user_id = {message.author.id}")
                user_id = maxergdb_cursor.fetchone()

                if user_id is None:
                    instert_new_user_id = "INSERT INTO maxerg_levels (user_id, experience, berichten, level) VALUES (%s, %s, %s, %s)"
                    lvl_record = (message.author.id, random_exp, 1, 0)
                    maxergdb_cursor.execute(instert_new_user_id, lvl_record)
                    db_maxerg.commit()
                    experience = random_exp
                else:
                    maxergdb_cursor.execute(f"SELECT experience FROM maxerg_levels WHERE user_id = {message.author.id}")
                    exp = maxergdb_cursor.fetchone()
                    experience = exp[0] + random_exp

                    maxergdb_cursor.execute(f"UPDATE maxerg_levels SET experience = experience + {random_exp} WHERE user_id = {message.author.id}")
                    maxergdb_cursor.execute(f"UPDATE maxerg_levels SET berichten = berichten + 1 WHERE user_id = {message.author.id}")
                    db_maxerg.commit()

                maxergdb_cursor.execute(f"SELECT level FROM maxerg_levels WHERE user_id = {message.author.id}")
                lvl_start_tuple = maxergdb_cursor.fetchone()
                lvl_start = lvl_start_tuple[0]

                level_up_channel = self.client.get_channel(563347368037056513)
                lvl_end = int(experience ** (1 / 3.3))  # experience ** (1 / 3.3)
                if lvl_start < lvl_end:
                    if lvl_end >= 5:
                        role = get(message.guild.roles, id=714036438659760159)
                        await message.author.add_roles(role)
                    if lvl_end >= 10:
                        role = get(message.guild.roles, id=714036464404398094)
                        await message.author.add_roles(role)
                    if lvl_end >= 20:
                        role = get(message.guild.roles, id=714036480724566057)
                        await message.author.add_roles(role)
                    if lvl_end >= 25:
                        role = get(message.guild.roles, id=714036496960847902)
                        await message.author.add_roles(role)
                    if lvl_end >= 30:
                        role = get(message.guild.roles, id=773957810135760956)
                        await message.author.add_roles(role)

                    level_up_embed = discord.Embed(
                        title=f"{message.author.display_name}",
                        description=f"{message.author.mention} is nu level **{lvl_end}**!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    level_up_embed.set_thumbnail(url=message.author.avatar_url)
                    level_up_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    level_up_embed.set_footer(text=footer)
                    await level_up_channel.send(embed=level_up_embed)

                    maxergdb_cursor.execute(f"UPDATE maxerg_levels SET level = {lvl_end} WHERE user_id = {message.author.id}")
                    db_maxerg.commit()

                random_money = randint(4, 12)
                maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_economie WHERE user_id = {message.author.id}")
                user_id_eco = maxergdb_cursor.fetchone()

                if user_id_eco is None:
                    insert_new_user_id_eco = "INSERT INTO maxerg_economie (user_id, cash, bank, netto, prestige, job, max_bank) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    ecogame_record = (message.author.id, 0, 0, 0, 0, "werkloos", 5000)
                    maxergdb_cursor.execute(insert_new_user_id_eco, ecogame_record)
                    db_maxerg.commit()
                else:
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET cash = cash + {random_money}, netto = netto + {random_money} WHERE user_id = {message.author.id}")
                    db_maxerg.commit()
                db_maxerg.close()

    @commands.command(aliases=["level"])
    async def rank(self, ctx, *, member: discord.Member = None):
        if str(ctx.channel) in command_channels:
            if member is None:
                member = ctx.author

            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_levels WHERE user_id = {member.id}")
            lvl_data = maxergdb_cursor.fetchone()
            level = lvl_data[3]
            berichten = lvl_data[2]
            exp = lvl_data[1]
            db_maxerg.close()

            voortgang = round(exp ** (1 / 3.5), 1)
            oude_voortgang = voortgang % int(voortgang)
            oude_voortgang = oude_voortgang * 10
            voortgang = int(oude_voortgang) * 2

            voortgang_bar = "❚" * voortgang
            lengte_bar = len(voortgang_bar)
            rest = 20-lengte_bar
            rest_bar = "❘" * rest

            procent_voortgang = round(exp ** (1 / 3.5), 2)
            procent_voortgang = procent_voortgang % int(procent_voortgang)
            procent = round(procent_voortgang * 100)

            voortgang = f"{voortgang_bar}{rest_bar} ➼ {procent}%"

            level_embed = discord.Embed(
                title=f"{member.display_name}",
                description=f"**Voortgang**\n{voortgang}",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            level_embed.add_field(name="Level", value=f"{level}", inline=True)
            level_embed.add_field(name="Berichten", value=f"{berichten}", inline=True)
            level_embed.set_thumbnail(url=member.avatar_url)
            level_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            level_embed.set_footer(text=footer)
            await ctx.send(embed=level_embed)

    @commands.command()
    async def levels(self, ctx, page=1):
        if str(ctx.channel) in command_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            offset = (page - 1) * 10
            leaderboard_zin = ""
            volgnummer = offset

            langste_regel = 0

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_levels ORDER BY berichten DESC LIMIT 10 OFFSET {offset}")
            result = maxergdb_cursor.fetchall()
            for row in result:
                volgnummer = volgnummer + 1
                volgnummer_prefix = f"{volgnummer}."
                lengte_volgnummer_prefix = len(volgnummer_prefix)
                aantal_spaties = 6 - lengte_volgnummer_prefix
                spatie_prefix = " " * aantal_spaties
                volgnummer_prefix = spatie_prefix + volgnummer_prefix

                try:
                    top_names = self.client.get_user(row[0])
                except AttributeError:
                    top_names = "Onbekend#0000"

                aantal_berichten = row[2]
                lengte_aantal_berichten = len(str(aantal_berichten))
                aantal_spaties = 9 - lengte_aantal_berichten
                spatie_prefix = " " * aantal_spaties
                aantal_berichten_prefix = spatie_prefix + str(aantal_berichten)

                nieuwe_zin = f"{volgnummer_prefix} | {aantal_berichten_prefix} | {top_names}\n"
                leaderboard_zin = leaderboard_zin + nieuwe_zin

                if len(nieuwe_zin) > langste_regel:
                    langste_regel = len(nieuwe_zin)

            if leaderboard_zin == "":
                leaderboard_zin = "Geen data gevonden!"

            maxergdb_cursor.execute(f"SELECT berichten FROM maxerg_levels WHERE berichten != 0")
            max_pages_tuple = maxergdb_cursor.fetchall()
            max_pages = len(max_pages_tuple)

            if max_pages % 10 != 0:
                max_pages = max_pages // 10 + 1
            else:
                max_pages = max_pages // 10

            header = "Plaats | Berichten | Gebruiker"

            if len(header) > langste_regel:
                langste_regel = len(header)

            seperator = "=" * langste_regel

            embed = discord.Embed(
                title=f"Leaderboard Levels",
                description=f"```md\n"
                            f"{header}\n{seperator}\n{leaderboard_zin}"
                            f"\n```",
                color=embedcolor
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=f"{footer} | Pagina {page}/{max_pages}")
            leaderboard_message = await ctx.send(embed=embed)

            await leaderboard_message.add_reaction("◀️")
            await leaderboard_message.add_reaction("▶️")

            def check(reaction, member):
                return member == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

            while True:
                try:
                    reaction, member = await self.client.wait_for("reaction_add", timeout=30, check=check)

                    if str(reaction.emoji) == "▶️" and page != max_pages:
                        page += 1
                        await leaderboard_message.remove_reaction(reaction, member)
                        nieuwe_pagina = True
                    elif str(reaction.emoji) == "◀️" and page > 1:
                        page -= 1
                        await leaderboard_message.remove_reaction(reaction, member)
                        nieuwe_pagina = True
                    else:
                        await leaderboard_message.remove_reaction(reaction, member)
                        nieuwe_pagina = False

                    if nieuwe_pagina:
                        offset = (page - 1) * 10
                        leaderboard_zin = ""
                        volgnummer = offset

                        maxergdb_cursor.execute(f"SELECT * FROM maxerg_levels ORDER BY berichten DESC LIMIT 10 OFFSET {offset}")
                        result = maxergdb_cursor.fetchall()
                        for row in result:
                            volgnummer = volgnummer + 1
                            volgnummer_prefix = f"{volgnummer}."
                            lengte_volgnummer_prefix = len(volgnummer_prefix)
                            aantal_spaties = 6 - lengte_volgnummer_prefix
                            spatie_prefix = " " * aantal_spaties
                            volgnummer_prefix = spatie_prefix + volgnummer_prefix

                            try:
                                top_names = self.client.get_user(row[0])
                            except AttributeError:
                                top_names = "Onbekend#0000"

                            aantal_berichten = row[2]
                            lengte_aantal_berichten = len(str(aantal_berichten))
                            aantal_spaties = 9 - lengte_aantal_berichten
                            spatie_prefix = " " * aantal_spaties
                            aantal_berichten_prefix = spatie_prefix + str(aantal_berichten)

                            nieuwe_zin = f"{volgnummer_prefix} | {aantal_berichten_prefix} | {top_names}\n"
                            leaderboard_zin = leaderboard_zin + nieuwe_zin

                            if len(nieuwe_zin) > langste_regel:
                                langste_regel = len(nieuwe_zin)

                        if leaderboard_zin == "":
                            leaderboard_zin = "Geen data gevonden!"

                        if len(header) > langste_regel:
                            langste_regel = len(header)

                        seperator = "=" * langste_regel

                        embed = discord.Embed(
                            title=f"Leaderboard Levels",
                            description=f"```md\n"
                                        f"{header}\n{seperator}\n{leaderboard_zin}"
                                        f"\n```",
                            color=embedcolor
                        )
                        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        embed.set_footer(text=f"{footer} | Pagina {page}/{max_pages}")
                        await leaderboard_message.edit(embed=embed)
                except asyncio.TimeoutError:
                    await leaderboard_message.clear_reaction("◀️")
                    await leaderboard_message.clear_reaction("▶️")
                    break
            db_maxerg.close()


def setup(client):
    client.add_cog(LevelingSystem(client))
