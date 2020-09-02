import discord
from discord.ext import commands
import json
import asyncio
from discord.ext.commands import MissingPermissions
from discord.utils import get
import datetime
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


class AutoModerator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["overtredingen"])
    @commands.has_permissions(kick_members=True)
    async def interfractions(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        maxergdb_cursor.execute(f"SELECT count FROM maxerg_modlogs WHERE user_id = {member.id}")
        interfraction_tuple = maxergdb_cursor.fetchone()

        if interfraction_tuple is None:
            sql_insert_modlogs = "INSERT INTO maxerg_modlogs (user_id, count) VALUES (%s, %s)"
            record = (f"{member.id}", 0)
            maxergdb_cursor.execute(sql_insert_modlogs, record)
            db_maxerg.commit()

            interfraction = 0
        else:
            interfraction = interfraction_tuple[0]

        if interfraction == 1:
            overtredingen = "overtreding"
        else:
            overtredingen = "overtredingen"

        embed = discord.Embed(
            title=f"Overtredingen",
            description=f"{member.display_name} heeft {interfraction} {overtredingen}!",
            color=embed_color,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=embed_footer)
        await ctx.send(embed=embed)
        db_maxerg.close()

    @interfractions.error
    async def interfractions_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        verboden_links = ['discord.gg', 'https://discord.gg/', 'https://discord.com/invite/', 'https://disboard.org/',
                          'https://top.gg/', 'https://discordservers.me/', 'https://discord.me/',
                          'https://discordservers.com/']

        staff_channels = ["🔒│staff", "🤑│partners", "📋│tickets"]

        if str(message.channel) not in staff_channels:
            admin_role = get(message.guild.roles, name="🔥│Sr. Moderator")
            if admin_role not in message.author.roles:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                mod_maxergdb_cursor = db_maxerg.cursor()

                mod_maxergdb_cursor.execute(
                    f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_member_ids = {message.author.id} AND ticket_channel_ids = {message.channel.id}")
                channel_id_list = mod_maxergdb_cursor.fetchone()

                if channel_id_list is not None and message.channel.id != channel_id_list[0]:
                    for link in verboden_links:
                        if message.content.count(link) > 0:
                            await message.channel.purge(limit=1)
                            counter_message2 = await message.channel.send(
                                f"HEY! Deze link is verboden, {message.author.mention}!")

                            log_channel = self.client.get_channel(561243076450975754)
                            embed = discord.Embed(
                                color=embed_color,
                                timestamp=datetime.datetime.utcnow()
                            )
                            embed.add_field(name="Gebruiker",
                                            value=f"**Naam:** {message.author.mention}\n**ID:** {message.author.id}",
                                            inline=False)
                            embed.add_field(name="Bericht", value=f"{message.content}", inline=False)
                            embed.set_author(name=f"[AUTOMODERATIE] {message.author}", icon_url=message.author.avatar_url)
                            embed.set_thumbnail(url=message.author.avatar_url)
                            embed.set_footer(text=embed_footer)
                            await log_channel.send(embed=embed)

                            mod_maxergdb_cursor.execute(f"SELECT count FROM maxerg_modlogs WHERE user_id = {message.author.id}")
                            interfraction_tuple = mod_maxergdb_cursor.fetchone()

                            if interfraction_tuple is None:
                                sql_insert_modlogs = "INSERT INTO maxerg_modlogs (user_id, count) VALUES (%s, %s)"
                                record = (f"{message.author.id}", 1)
                                mod_maxergdb_cursor.execute(sql_insert_modlogs, record)
                                db_maxerg.commit()
                            else:
                                new_count = interfraction_tuple[0] + 1
                                sql_update_modlogs = f"UPDATE maxerg_modlogs SET count = {new_count} WHERE user_id = {message.author.id}"
                                mod_maxergdb_cursor.execute(sql_update_modlogs)
                                db_maxerg.commit()

                                if new_count % 5 == 0:
                                    role_check = discord.utils.find(lambda r: r.name == 'Muted', message.guild.roles)
                                    if role_check not in message.author.roles:
                                        role = get(message.guild.roles, name="Muted")
                                        await message.author.add_roles(role)

                                        premute_embed = discord.Embed(
                                            description=f"**Reden:** Automoderatie\n**Duratie:** 24u",
                                            color=embed_color
                                        )
                                        premute_embed.set_author(name=f"{message.author} is gemute!",
                                                                 icon_url=message.author.avatar_url)
                                        await message.channel.send(embed=premute_embed)

                                        log_channel = self.client.get_channel(561243076450975754)

                                        mute_embed = discord.Embed(
                                            color=embed_color,
                                            timestamp=datetime.datetime.utcnow()
                                        )
                                        mute_embed.add_field(name="Gebruiker",
                                                             value=f"**Naam:**\t{message.author.mention}\n**ID:**\t{message.author.id}",
                                                             inline=True)
                                        mute_embed.add_field(name="Moderator",
                                                             value=f"**Naam:**\t{self.client.user.mention}\n**ID:**\t{self.client.user.id}",
                                                             inline=True)
                                        mute_embed.add_field(name="Reden", value=f"Automoderatie", inline=False)
                                        mute_embed.add_field(name="Duur", value="24 uur", inline=False)
                                        mute_embed.set_author(name=f"[TEMPMUTE] {message.author}",
                                                              icon_url=message.author.avatar_url)
                                        mute_embed.set_footer(text=embed_footer[0])
                                        await log_channel.send(embed=mute_embed)

                                        await asyncio.sleep(86400)

                                        role_check = discord.utils.find(lambda r: r.name == 'Muted', message.guild.roles)
                                        if role_check in message.author.roles:
                                            role = discord.utils.get(message.guild.roles, name="Muted")
                                            await message.author.remove_roles(role)

                                            log_channel = self.client.get_channel(561243076450975754)

                                            unmute_embed = discord.Embed(
                                                color=embed_color,
                                                timestamp=datetime.datetime.utcnow()
                                            )
                                            unmute_embed.add_field(name="Gebruiker",
                                                                   value=f"**Naam:**\t{message.author.mention}\n**ID:**\t{message.author.id}",
                                                                   inline=True)
                                            unmute_embed.add_field(name="Moderator",
                                                                   value=f"**Naam:**\t{self.client.user.mention}\n**ID:**\t{self.client.user.id}",
                                                                   inline=True)
                                            unmute_embed.set_author(name=f"[UNMUTE] {message.author}",
                                                                    icon_url=message.author.avatar_url)
                                            unmute_embed.set_footer(text=embed_footer[0])
                                            await log_channel.send(embed=unmute_embed)
                            await asyncio.sleep(3)
                            await counter_message2.delete()
                db_maxerg.close()


def setup(client):
    client.add_cog(AutoModerator(client))
