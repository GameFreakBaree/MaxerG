import discord
from discord.ext import commands
import json
import datetime
from discord.utils import get
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


class Informatie(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        command_channels = ["🤖│commands", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            db_maxerg.commit()
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            if member is None:
                member = ctx.author

            joined_correct = member.joined_at.strftime("%d/%m/%Y")

            overlordrole = get(member.guild.roles, name="Overlord")
            godrole = get(member.guild.roles, name="God")
            titanrole = get(member.guild.roles, name="Titan")
            lordrole = get(member.guild.roles, name="Lord")

            if overlordrole in member.roles:
                overlord_emote = "✅"
            else:
                overlord_emote = ":x:"

            if godrole in member.roles:
                god_emote = "✅"
            else:
                god_emote = ":x:"

            if titanrole in member.roles:
                titan_emote = "✅"
            else:
                titan_emote = ":x:"

            if lordrole in member.roles:
                lord_emote = "✅"
            else:
                lord_emote = ":x:"

            maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_levels WHERE user_id = {member.id}")
            user_id = maxergdb_cursor.fetchone()

            if user_id is None:
                instert_new_user_id = "INSERT INTO maxerg_levels (user_id, experience, berichten, level) VALUES (%s, %s, %s, %s)"
                lvl_record = (member.id, 0, 0, 0)
                maxergdb_cursor.execute(instert_new_user_id, lvl_record)
                db_maxerg.commit()

            maxergdb_cursor.execute(f"SELECT berichten FROM maxerg_levels WHERE user_id = {member.id}")
            berichten = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute(f"SELECT level FROM maxerg_levels WHERE user_id = {member.id}")
            level_check = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute(f"SELECT count FROM maxerg_modlogs WHERE user_id = {member.id}")
            interfractions_tuple = maxergdb_cursor.fetchone()

            if interfractions_tuple is None:
                interfractions = 0
            else:
                interfractions = interfractions_tuple[0]

            info_embed = discord.Embed(
                title=f"{member.display_name}",
                timestamp=datetime.datetime.utcnow(),
                color=embed_color
            )
            info_embed.add_field(name="Gebruiker Info",
                                 value=f"ID: {member.id}\n"
                                       f"Gebruikersnaam: {member.display_name}\nTAG: #{member.discriminator}",
                                 inline=False)
            info_embed.add_field(name="Gejoined op", value=joined_correct, inline=True)
            info_embed.add_field(name="Level", value=f"{level_check[0]}", inline=True)
            info_embed.add_field(name="Berichten", value=f"{berichten[0]}", inline=True)
            info_embed.add_field(name="Waarschuwingen", value=f"{interfractions}", inline=False)
            info_embed.add_field(name="Hoogste Rank", value=member.top_role, inline=True)
            info_embed.add_field(name="Ranks:", value=f"{overlord_emote} Overlord\n{god_emote} God"
                                                      f"\n{titan_emote} Titan\n{lord_emote} Lord\n", inline=True)
            info_embed.set_thumbnail(url=member.avatar_url)
            info_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            info_embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=info_embed)


def setup(client):
    client.add_cog(Informatie(client))
