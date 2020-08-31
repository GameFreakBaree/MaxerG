import discord
from discord.ext import commands
import json
from discord.ext.commands import BadArgument
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

maxergdb_cursor = db_maxerg.cursor()

maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
embed_footer = maxergdb_cursor.fetchone()

maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
embed_color_tuple = maxergdb_cursor.fetchone()
embed_color = int(embed_color_tuple[0], 16)


async def ticket_create(self, bericht, member, args, cmd):
    await self.client.wait_until_ready()

    if args is None:
        message_content = "Niet Vermeld"
    else:
        message_content = f"{args}"

    maxergdb_cursor.execute("SELECT ticket_nr FROM maxerg_ticket_config")
    ticket_nr = maxergdb_cursor.fetchone()
    ticket_number = ticket_nr[0]
    ticket_number += 1

    sql_ticketnr = f"UPDATE maxerg_ticket_config SET ticket_nr = {ticket_number} WHERE ticket_nr = {ticket_number - 1}"
    maxergdb_cursor.execute(sql_ticketnr)
    db_maxerg.commit()

    ticket_cat = "▬▬ Tickets ▬▬"
    ticket_category = get(bericht.guild.categories, name=ticket_cat)

    ticket_channel = await bericht.guild.create_text_channel(f"ticket-{ticket_number:04}", category=ticket_category)
    await ticket_channel.set_permissions(bericht.guild.get_role(bericht.guild.id), send_messages=False,
                                         read_messages=False)

    role = bericht.guild.get_role(721050870590210149)
    await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True,
                                         embed_links=True, attach_files=True, read_message_history=True,
                                         external_emojis=True)

    await ticket_channel.set_permissions(member, send_messages=True, read_messages=True, add_reactions=True,
                                         embed_links=True, attach_files=True, read_message_history=True,
                                         external_emojis=True)

    if cmd is not None:
        embed = discord.Embed(
            description=f"Je ticket is aangemaakt! <#{ticket_channel.id}>",
            color=embed_color
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=embed_footer[0])
        await bericht.send(embed=embed)

    ticket_embed = discord.Embed(
        description=f"Bedankt voor het maken van een ticket! We zullen zo snel mogelijk antwoorden.\n"
                    f"Tag ons niet want dat vertraagd het antwoorden alleen maar.\n\n"
                    f"Ticket Eigenaar: {member.mention}\n**Reden:** {message_content}",
        color=embed_color
    )
    ticket_embed.add_field(name="Ticket Commands", value="!add <naam>\n!remove <naam>\n!close", inline=False)
    ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
    ticket_embed.set_thumbnail(url=member.avatar_url)
    ticket_embed.set_footer(text=embed_footer[0])
    await ticket_channel.send(embed=ticket_embed)

    sql_ids = f"INSERT INTO maxerg_tickets (ticket_channel_ids, ticket_member_ids) VALUES (%s, %s)"
    record = (f"{ticket_channel.id}", f"{member.id}")
    maxergdb_cursor.execute(sql_ids, record)
    db_maxerg.commit()


class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        db_maxerg.commit()
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        maxergdb_cursor.execute("SELECT ticket_message_id FROM maxerg_ticket_config")
        setup_message_id_tuple = maxergdb_cursor.fetchone()
        setup_message_id = setup_message_id_tuple[0]

        maxergdb_cursor.execute("SELECT ticket_channel_id FROM maxerg_ticket_config")
        setup_channel_id_tuple = maxergdb_cursor.fetchone()
        setup_channel_id = setup_channel_id_tuple[0]

        if not member.bot:
            if message_id == setup_message_id:
                if payload.emoji.name == "check":
                    maxergdb_cursor.execute(f"SELECT ticket_member_ids FROM maxerg_tickets WHERE ticket_member_ids = {member.id}")
                    user_id = maxergdb_cursor.fetchone()

                    if user_id is not None:
                        gebruiker_getinfo = self.client.get_user(member.id)
                        bericht = await self.client.get_channel(setup_channel_id).fetch_message(setup_message_id)
                        await gebruiker_getinfo.send("Je hebt al een ticket open.")
                        await bericht.remove_reaction(emoji='check:725030739543982240', member=member)
                    else:
                        args = None
                        bericht = await self.client.get_channel(setup_channel_id).fetch_message(setup_message_id)
                        await ticket_create(self, bericht, member, args, cmd=None)
                        await bericht.remove_reaction(emoji='check:725030739543982240', member=member)

    @commands.command(aliases=["ticket"])
    async def new(self, ctx, *, args=None):
        command_channels = ["🤖│commands", "🔒│bots"]
        if str(ctx.channel) in command_channels:
            db_maxerg.commit()
            maxergdb_cursor.execute(
                f"SELECT ticket_member_ids FROM maxerg_tickets WHERE ticket_member_ids = {ctx.author.id}")
            member_id_list = maxergdb_cursor.fetchone()

            if member_id_list is None:
                await self.client.wait_until_ready()

                cmd = 1
                await ticket_create(self, ctx, ctx.author, args, cmd)
            elif ctx.author.id == member_id_list[0]:
                await ctx.author.send("Je hebt al een ticket open.")
                await ctx.message.delete()
            else:
                print("Error in Ticket Cmd NEW")

    @commands.command()
    async def close(self, ctx):
        db_maxerg.commit()
        maxergdb_cursor.execute(
            f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_member_ids = {ctx.author.id} AND ticket_channel_ids = {ctx.channel.id}")
        channel_id_list = maxergdb_cursor.fetchone()

        if channel_id_list is not None:
            if ctx.channel.id == channel_id_list[0]:
                await ctx.channel.delete()

                drop_sql_tickets = f"DELETE FROM maxerg_tickets WHERE ticket_member_ids = {ctx.author.id} AND ticket_channel_ids = {ctx.channel.id}"
                maxergdb_cursor.execute(drop_sql_tickets)
                db_maxerg.commit()

    @commands.command()
    async def add(self, ctx, member: discord.Member = None):
        db_maxerg.commit()
        maxergdb_cursor.execute(
            f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_member_ids = {ctx.author.id} AND ticket_channel_ids = {ctx.channel.id}")
        channel_id_list = maxergdb_cursor.fetchone()

        if channel_id_list is not None:
            if ctx.channel.id == channel_id_list[0]:
                ticket_channel = ctx.message.channel
                await ticket_channel.set_permissions(
                    member, send_messages=True, read_messages=True, add_reactions=True, embed_links=True,
                    attach_files=True, read_message_history=True, external_emojis=True
                )

                ticket_embed = discord.Embed(
                    description=f"{member.mention} is toegevoegd aan dit ticket!",
                    color=embed_color
                )
                ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                ticket_embed.set_thumbnail(url=member.avatar_url)
                ticket_embed.set_footer(text=embed_footer[0])
                await ctx.send(embed=ticket_embed)

    @commands.command()
    async def remove(self, ctx, member: discord.Member = None):
        db_maxerg.commit()
        maxergdb_cursor.execute(
            f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_member_ids = {ctx.author.id} AND ticket_channel_ids = {ctx.channel.id}")
        channel_id_list = maxergdb_cursor.fetchone()

        if channel_id_list is not None:
            if ctx.channel.id == channel_id_list[0]:
                ticket_channel = ctx.message.channel

                await ticket_channel.set_permissions(member, send_messages=False, read_messages=False,
                                                     add_reactions=False, embed_links=False, attach_files=False,
                                                     read_message_history=False, external_emojis=False)

                ticket_embed = discord.Embed(
                    description=f"{member.mention} is verwijderd van dit ticket!",
                    color=embed_color
                )
                ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                ticket_embed.set_thumbnail(url=member.avatar_url)
                ticket_embed.set_footer(text=embed_footer[0])
                await ctx.send(embed=ticket_embed)

    @commands.command()
    async def rename(self, ctx, rename_value=None):
        mod_role = get(ctx.guild.roles, name="🔥│Sr. Moderator")
        if mod_role in ctx.author.roles:
            if rename_value is not None:
                db_maxerg.commit()
                maxergdb_cursor.execute(
                    f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
                channel_id = maxergdb_cursor.fetchone()

                if channel_id is not None:
                    if ctx.message.channel.id == channel_id[0]:
                        await ctx.channel.purge(limit=1)
                        rename_channel = ctx.message.channel

                        rename_channel_str = str(rename_channel)
                        ticket_number = rename_channel_str[-4:]

                        await rename_channel.edit(name=f"{rename_value.lower()}-{ticket_number}")

    @commands.command(name="force-rename")
    async def force_rename(self, ctx, rename_value=None):
        mod_role = get(ctx.guild.roles, name="🔥│Sr. Moderator")
        if mod_role in ctx.author.roles:
            if rename_value is not None:
                db_maxerg.commit()
                maxergdb_cursor.execute(
                    f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
                channel_id = maxergdb_cursor.fetchone()

                if channel_id is not None:
                    if ctx.message.channel.id == channel_id[0]:
                        await ctx.channel.purge(limit=1)
                        rename_channel = ctx.message.channel

                        await rename_channel.edit(name=f"{rename_value.lower()}")

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                description="**Error!** De opgegeven gebruiker is niet gevonden.",
                color=embed_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                description="**Error!** De opgegeven gebruiker is niet gevonden.",
                color=embed_color
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=embed_footer[0])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ticket(client))
