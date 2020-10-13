import discord
from discord.ext import commands
from discord.ext.commands import BadArgument
from discord.utils import get
import mysql.connector
from settings import host, user, password, database, embedcolor, footer

emote_list = ['1️⃣', '2️⃣', '3️⃣']


async def ticket_create(self, bericht, member, db_maxerg, maxergdb_cursor, reactie):
    await self.client.wait_until_ready()

    if reactie == "2️⃣":
        reden = "Staff Sollicitatie"
    elif reactie == "3️⃣":
        reden = "Partner Aanvraag"
    else:
        reden = "Algemeen"

    maxergdb_cursor.execute("SELECT ticket_nr FROM maxerg_ticket_config")
    ticket_nr = maxergdb_cursor.fetchone()
    ticket_number = ticket_nr[0]
    ticket_number += 1

    maxergdb_cursor.execute(f"UPDATE maxerg_ticket_config SET ticket_nr = {ticket_number} WHERE ticket_nr = {ticket_number - 1}")
    db_maxerg.commit()

    ticket_cat = "▬▬ Tickets ▬▬"
    ticket_category = get(bericht.guild.categories, name=ticket_cat)

    ticket_channel = await bericht.guild.create_text_channel(f"ticket-{ticket_number:04}", category=ticket_category, topic=f"Reden: {reden}")
    await ticket_channel.set_permissions(bericht.guild.get_role(bericht.guild.id), send_messages=False, read_messages=False)

    if reactie == "one":
        role = bericht.guild.get_role(721050870590210149)
        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True,
                                             embed_links=True, attach_files=True, read_message_history=True,
                                             external_emojis=True)

    await ticket_channel.set_permissions(member, send_messages=True, read_messages=True, add_reactions=True,
                                         embed_links=True, attach_files=True, read_message_history=True,
                                         external_emojis=True)

    ticket_embed = discord.Embed(
        description=f"Bedankt voor het maken van een ticket! We zullen zo snel mogelijk antwoorden.\n"
                    f"Tag ons niet want dat vertraagd het antwoorden alleen maar.\n\n"
                    f"Ticket Eigenaar: {member.mention}\n**Reden:** {reden}",
        color=embedcolor
    )
    ticket_embed.add_field(name="Ticket Commands", value="!add <naam>\n!remove <naam>\n!close", inline=False)
    ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
    ticket_embed.set_thumbnail(url=member.avatar_url)
    ticket_embed.set_footer(text=footer)
    await ticket_channel.send(embed=ticket_embed)

    if reactie == "2️⃣":
        await ticket_channel.send("Voltooi deze stappen om een kans te maken op een staff positie:"
                                  "\n\n**1.** Vul **<https://jobs.maxerg.net/>** in."
                                  "\n**2.** Geef een paar datums en tijden mee wanneer je op sollicitatie gesprek kan."
                                  "\n**3.** Bereidt je voor op een goed sollicitatie gesprek.")
    elif reactie == "3️⃣":
        await ticket_channel.send("Voltooi deze stappen om een kans te maken op een partnership:"
                                  "\n\n**1.** Meer dan 75 MENSEN in je discord server hebben."
                                  "\n**2.** Stuur een PERMANENTE link van je discord server."
                                  "\n**3.** Vertel waarom je een partnership wilt aangaan.")

    sql_ids = f"INSERT INTO maxerg_tickets (ticket_channel_ids, ticket_member_ids) VALUES (%s, %s)"
    record = (f"{ticket_channel.id}", f"{member.id}")
    maxergdb_cursor.execute(sql_ids, record)
    db_maxerg.commit()
    return ticket_channel


class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        await ctx.channel.purge(limit=2)
        em = discord.Embed(
            title=f"🎫 Tickets",
            description=f"Klik op de reacties hieronder om een ticket aan te maken!\n"
                        f"Kies de gepaste reactie voor jouw ticket.\n\n"
                        f":one: Algemeen\n"
                        f":two: Staff Sollicitatie\n"
                        f":three: Partner Aanvraag",
            color=embedcolor
        )
        em.set_footer(text=footer)
        embed = await ctx.send(embed=em)

        for emote in emote_list:
            await embed.add_reaction(emoji=emote)

        maxergdb_cursor.execute(f"UPDATE maxerg_ticket_config SET ticket_message_id = {embed.id}")
        maxergdb_cursor.execute(f"UPDATE maxerg_ticket_config SET ticket_channel_id = {embed.channel.id}")
        db_maxerg.commit()
        db_maxerg.close()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        message_id = payload.message_id
        member = payload.user_id
        member = self.client.get_user(member)

        maxergdb_cursor.execute("SELECT ticket_message_id FROM maxerg_ticket_config")
        setup_message_id_tuple = maxergdb_cursor.fetchone()
        setup_message_id = setup_message_id_tuple[0]

        maxergdb_cursor.execute("SELECT ticket_channel_id FROM maxerg_ticket_config")
        setup_channel_id_tuple = maxergdb_cursor.fetchone()
        setup_channel_id = setup_channel_id_tuple[0]

        if not member.bot:
            if message_id == setup_message_id:
                if payload.emoji.name in emote_list:
                    maxergdb_cursor.execute(f"SELECT ticket_member_ids FROM maxerg_tickets WHERE ticket_member_ids = {member.id}")
                    user_id = maxergdb_cursor.fetchone()

                    if user_id is not None:
                        gebruiker_getinfo = self.client.get_user(member.id)
                        bericht = await self.client.get_channel(setup_channel_id).fetch_message(setup_message_id)
                        await gebruiker_getinfo.send("Je hebt al een ticket open.")
                        for emote in emote_list:
                            await bericht.remove_reaction(emoji=emote, member=member)
                    else:
                        bericht = await self.client.get_channel(setup_channel_id).fetch_message(setup_message_id)
                        await ticket_create(self, bericht, member, db_maxerg, maxergdb_cursor, payload.emoji.name)
                        for emote in emote_list:
                            await bericht.remove_reaction(emoji=emote, member=member)
        db_maxerg.close()

    @commands.command()
    async def close(self, ctx):
        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        maxergdb_cursor.execute(f"SELECT * FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
        channel_id_list = maxergdb_cursor.fetchone()

        staff_role = get(ctx.guild.roles, name="TicketStaff")
        if channel_id_list is not None:
            if staff_role in ctx.author.roles or ctx.author.id == channel_id_list[1]:
                await ctx.channel.delete()

                maxergdb_cursor.execute(f"DELETE FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
                db_maxerg.commit()
        db_maxerg.close()

    @commands.command()
    async def add(self, ctx, member: discord.Member = None):
        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        maxergdb_cursor.execute(f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
        channel_id_list = maxergdb_cursor.fetchone()
        db_maxerg.close()

        staff_role = get(ctx.guild.roles, name="TicketStaff")
        if channel_id_list is not None:
            if staff_role in ctx.author.roles or ctx.author.id == channel_id_list[1]:
                if ctx.channel.id == channel_id_list[0]:
                    ticket_channel = ctx.message.channel
                    await ticket_channel.set_permissions(member, send_messages=True, read_messages=True,
                                                         add_reactions=True, embed_links=True, attach_files=True,
                                                         read_message_history=True, external_emojis=True)

                    ticket_embed = discord.Embed(
                        description=f"{member.mention} is toegevoegd aan dit ticket!",
                        color=embedcolor
                    )
                    ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    ticket_embed.set_thumbnail(url=member.avatar_url)
                    ticket_embed.set_footer(text=footer)
                    await ctx.send(embed=ticket_embed)

    @commands.command()
    async def remove(self, ctx, member: discord.Member = None):
        db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
        maxergdb_cursor = db_maxerg.cursor()

        maxergdb_cursor.execute(f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
        channel_id_list = maxergdb_cursor.fetchone()
        db_maxerg.close()

        staff_role = get(ctx.guild.roles, name="TicketStaff")
        if channel_id_list is not None:
            if staff_role in ctx.author.roles or ctx.author.id == channel_id_list[1]:
                if ctx.channel.id == channel_id_list[0]:
                    ticket_channel = ctx.message.channel

                    await ticket_channel.set_permissions(member, send_messages=False, read_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False)

                    ticket_embed = discord.Embed(
                        description=f"{member.mention} is verwijderd van dit ticket!",
                        color=embedcolor
                    )
                    ticket_embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    ticket_embed.set_thumbnail(url=member.avatar_url)
                    ticket_embed.set_footer(text=footer)
                    await ctx.send(embed=ticket_embed)

    @commands.command()
    async def rename(self, ctx, rename_value=None):
        mod_role = get(ctx.guild.roles, name="🔥│Sr. Moderator")
        if mod_role in ctx.author.roles:
            if rename_value is not None:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
                channel_id = maxergdb_cursor.fetchone()
                db_maxerg.close()

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
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT ticket_channel_ids FROM maxerg_tickets WHERE ticket_channel_ids = {ctx.channel.id}")
                channel_id = maxergdb_cursor.fetchone()
                db_maxerg.close()

                if channel_id is not None:
                    if ctx.message.channel.id == channel_id[0]:
                        await ctx.channel.purge(limit=1)
                        rename_channel = ctx.message.channel

                        await rename_channel.edit(name=f"{rename_value.lower()}")

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                description="**Error!** De opgegeven gebruiker is niet gevonden.",
                color=embedcolor
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, BadArgument):
            embed = discord.Embed(
                description="**Error!** De opgegeven gebruiker is niet gevonden.",
                color=embedcolor
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ticket(client))
