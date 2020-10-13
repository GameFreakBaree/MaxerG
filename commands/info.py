import discord
from discord.ext import commands
import datetime
from discord.utils import get
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, command_channels


class Informatie(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if str(ctx.channel) in command_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            if member is None:
                member = ctx.author

            joined_correct = member.joined_at.strftime("%d/%m/%Y")

            lvl20_role = get(member.guild.roles, name="LvL.20")
            lvl15_role = get(member.guild.roles, name="LvL.15")
            lvl10_role = get(member.guild.roles, name="LvL.10")
            lvl5_role = get(member.guild.roles, name="LvL.5")

            if lvl20_role in member.roles:
                lvl20_emote = "✅"
            else:
                lvl20_emote = ":x:"

            if lvl15_role in member.roles:
                lvl15_emote = "✅"
            else:
                lvl15_emote = ":x:"

            if lvl10_role in member.roles:
                lvl10_emote = "✅"
            else:
                lvl10_emote = ":x:"

            if lvl5_role in member.roles:
                lvl5_emote = "✅"
            else:
                lvl5_emote = ":x:"

            maxergdb_cursor.execute(f"SELECT user_id FROM maxerg_levels WHERE user_id = {member.id}")
            user_id = maxergdb_cursor.fetchone()

            if user_id is None:
                berichten = (0,)
                level_check = (0,)
            else:
                maxergdb_cursor.execute(f"SELECT berichten FROM maxerg_levels WHERE user_id = {member.id}")
                berichten = maxergdb_cursor.fetchone()

                maxergdb_cursor.execute(f"SELECT level FROM maxerg_levels WHERE user_id = {member.id}")
                level_check = maxergdb_cursor.fetchone()

            info_embed = discord.Embed(
                title=f"{member.display_name}",
                timestamp=datetime.datetime.utcnow(),
                color=embedcolor
            )
            info_embed.add_field(name="Gebruiker Info",
                                 value=f"ID: {member.id}\n"
                                       f"Gebruikersnaam: {member.display_name}\nTAG: #{member.discriminator}",
                                 inline=False)
            info_embed.add_field(name="Gejoined op", value=joined_correct, inline=True)
            info_embed.add_field(name="Level", value=f"{level_check[0]}", inline=True)
            info_embed.add_field(name="Berichten", value=f"{berichten[0]}", inline=True)
            info_embed.add_field(name="Hoogste Rank", value=member.top_role, inline=True)
            info_embed.add_field(name="Ranks:", value=f"{lvl20_emote} Level 20+\n{lvl15_emote} Level 15+"
                                                      f"\n{lvl10_emote} Level 10+\n{lvl5_emote} Level 5+\n", inline=True)
            info_embed.set_thumbnail(url=member.avatar_url)
            info_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            info_embed.set_footer(text=footer)
            await ctx.send(embed=info_embed)
            db_maxerg.close()


def setup(client):
    client.add_cog(Informatie(client))
