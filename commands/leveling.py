import discord
from discord.ext import commands
import json
from random import randint
from discord.utils import get
import datetime
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()

db_maxerg = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    passwd=password
)

maxergdb_cursor = db_maxerg.cursor()

maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
embed_color_tuple = maxergdb_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)

maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
embed_footer = maxergdb_cursor.fetchone()


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
                return
            else:
                db_maxerg.commit()

                # dead_channels = ["📈│memes"]
                # if str(message.channel) in dead_channels:
                #     random_exp = randint(6, 14)
                # else:
                random_exp = randint(6, 14)

                maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_levels WHERE user_id = {message.author.id}")
                user_id = maxergdb_cursor.fetchone()

                if user_id is None:
                    with open('./old_data/levels.json', 'r') as f:
                        user_level_data = json.load(f)

                    if f'{message.author.id}' in user_level_data:
                        experience = user_level_data[f'{message.author.id}']['experience']
                        messages = user_level_data[f'{message.author.id}']['berichten']
                        lvl_start = user_level_data[f'{message.author.id}']['level']

                        if messages == 0:
                            messages = 1
                    else:
                        experience = 0
                        messages = 1
                        lvl_start = 0

                    exp_new_random = experience + random_exp

                    instert_new_user_id = "INSERT INTO maxerg_levels (user_id, experience, berichten, level) VALUES (%s, %s, %s, %s)"
                    lvl_record = (message.author.id, exp_new_random, messages, lvl_start)
                    maxergdb_cursor.execute(instert_new_user_id, lvl_record)
                    db_maxerg.commit()

                    experience = random_exp
                else:
                    maxergdb_cursor.execute(f"SELECT experience FROM maxerg_levels WHERE user_id = {message.author.id}")
                    exp = maxergdb_cursor.fetchone()
                    experience = exp[0] + random_exp

                    level_sql_exp = f"UPDATE maxerg_levels SET experience = experience + {random_exp} WHERE user_id = {message.author.id}"
                    maxergdb_cursor.execute(level_sql_exp)
                    db_maxerg.commit()

                    level_sql_berichten = f"UPDATE maxerg_levels SET berichten = berichten + 1 WHERE user_id = {message.author.id}"
                    maxergdb_cursor.execute(level_sql_berichten)
                    db_maxerg.commit()

                maxergdb_cursor.execute(f"SELECT level FROM maxerg_levels WHERE user_id = {message.author.id}")
                lvl_start_tuple = maxergdb_cursor.fetchone()
                lvl_start = lvl_start_tuple[0]

                level_up_channel = self.client.get_channel(747547955887603872)
                guild = message.guild
                lvl_end = int(experience ** (1 / 3.5))
                if lvl_start < lvl_end:
                    if lvl_end >= 5:
                        lordrole = get(guild.roles, name='LvL.5')
                        await message.author.add_roles(lordrole)
                    if lvl_end >= 10:
                        titanrole = get(guild.roles, name='LvL.10')
                        await message.author.add_roles(titanrole)
                    if lvl_end >= 15:
                        godrole = get(guild.roles, name='LvL.15')
                        await message.author.add_roles(godrole)
                    if lvl_end >= 20:
                        overlordrole = get(guild.roles, name='LvL.20')
                        await message.author.add_roles(overlordrole)

                    level_up_embed = discord.Embed(
                        title=f"{message.author.display_name}",
                        description=f"{message.author.mention} is nu level **{lvl_end}**!",
                        color=embed_color,
                        timestamp=datetime.datetime.utcnow()
                    )
                    level_up_embed.set_thumbnail(url=message.author.avatar_url)
                    level_up_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    level_up_embed.set_footer(text=embed_footer[0])
                    await level_up_channel.send(embed=level_up_embed)

                    level_sql_lvl = f"UPDATE maxerg_levels SET level = {lvl_end} WHERE user_id = {message.author.id}"
                    maxergdb_cursor.execute(level_sql_lvl)
                    db_maxerg.commit()

                random_money = randint(2, 8)

                maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_ecogame WHERE user_id = {message.author.id}")
                user_id_eco = maxergdb_cursor.fetchone()

                if user_id_eco is None:
                    with open('./old_data/ecogame.json', 'r') as f:
                        user_eco_data = json.load(f)

                    if f'{message.author.id}' in user_eco_data:
                        cash = user_eco_data[f'{message.author.id}']['cash']
                        bank = user_eco_data[f'{message.author.id}']['bank']
                    else:
                        cash = 0
                        bank = 0

                    cash_new_random = cash + random_money

                    instert_new_user_id_eco = "INSERT INTO maxerg_ecogame (user_id, cash, bank) VALUES (%s, %s, %s)"
                    ecogame_record = (message.author.id, cash_new_random, bank)
                    maxergdb_cursor.execute(instert_new_user_id_eco, ecogame_record)
                    db_maxerg.commit()
                else:
                    ecogame_sql_cash = f"UPDATE maxerg_ecogame SET cash = cash + {random_money} WHERE user_id = {message.author.id}"
                    maxergdb_cursor.execute(ecogame_sql_cash)
                    db_maxerg.commit()

    @commands.command(aliases=["level"])
    async def rank(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        command_channels = ["🤖│commands", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            db_maxerg.commit()

            maxergdb_cursor.execute(f"SELECT berichten FROM maxerg_levels WHERE user_id = {member.id}")
            berichten = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute(f"SELECT level FROM maxerg_levels WHERE user_id = {member.id}")
            level_check = maxergdb_cursor.fetchone()

            level_embed = discord.Embed(
                title=f"{member.display_name}",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            level_embed.add_field(name="Level", value=f"{level_check[0]}", inline=True)
            level_embed.add_field(name="Berichten", value=f"{berichten[0]}", inline=True)
            level_embed.set_thumbnail(url=member.avatar_url)
            level_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            level_embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=level_embed)

    @commands.command()
    async def levels(self, ctx, page=1):
        command_channels = ["🤖│commands", "🔒│bots", "🔒│staff"]
        if str(ctx.channel) in command_channels:
            db_maxerg.commit()

            pre_offset = page - 1
            offset = pre_offset * 10

            after_str = ""
            eerste_volgnummer = offset

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_levels ORDER BY berichten DESC LIMIT 10 OFFSET {offset}")
            result = maxergdb_cursor.fetchall()
            for row in result:
                eerste_volgnummer = eerste_volgnummer + 1

                try:
                    top_name = self.client.get_user(row[0])
                    top_names = top_name.mention
                except AttributeError:
                    top_names = row[0]

                top_aantal_berichten = row[2]
                if top_aantal_berichten == 1:
                    berichten = "bericht"
                else:
                    berichten = "berichten"

                pre_str = f"**{eerste_volgnummer}.** {top_names} • **{top_aantal_berichten}** {berichten}\n"
                after_str = after_str + pre_str

            if after_str == "":
                after_str = "Geen data gevonden!"

            alle_berichten = 0
            maxergdb_cursor.execute(f"SELECT berichten FROM maxerg_levels")
            berichtjes = maxergdb_cursor.fetchall()
            for row in berichtjes:
                alle_berichten = alle_berichten + row[0]

            embed = discord.Embed(
                title=f"Leaderboard [Pagina {page}]",
                description=f"__Totaal Berichten:__ {alle_berichten}\n\n{after_str}",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(LevelingSystem(client))
