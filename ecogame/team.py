import asyncio
import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels, prefix


class EcoTeam(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["teams"])
    async def team(self, ctx, setting=None, *, member: discord.Member = None):
        if str(ctx.channel) in ecogame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            if setting == "info" or setting == "help":
                em = discord.Embed(
                    title="Info: Team",
                    description=f"**Maximale Team grootte:** 3 (2 leden, 1 leider)"
                                f"\n\n**Commands gebruik:**"
                                f"\n`{prefix}team <optie> [naam]`"
                                f"\n\n**Commands:**"
                                f"\n• **{prefix}team info** - Bekijk deze embed."
                                f"\n• **{prefix}team maak** - Maak een team aan."
                                f"\n• **{prefix}team verwijder** - Verwijder je team."
                                f"\n• **{prefix}team verlaat** - Verlaat je team."
                                f"\n• **{prefix}team remove <naam>** - Verwijder iemand van je team."
                                f"\n• **{prefix}team invite <naam>** - Invite iemand in je team.",
                    color=embedcolor,
                    timestamp=datetime.datetime.utcnow()
                )
                em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                em.set_footer(text=footer)
                await ctx.send(embed=em)
            elif setting == "create" or setting == "maak":
                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE team_leader = {ctx.author.id} OR member_one = {ctx.author.id} OR member_two = {ctx.author.id}")
                teams_userdata = maxergdb_cursor.fetchone()

                if teams_userdata is None:
                    instertdata = "INSERT INTO maxerg_teams (team_leader, member_one, member_two) VALUES (%s, %s, %s)"
                    record = (ctx.author.id, 0, 0)
                    maxergdb_cursor.execute(instertdata, record)
                    db_maxerg.commit()

                    em = discord.Embed(
                        title="Team aangemaakt!",
                        description=f"**Team Leider:** {ctx.author.mention}\n**Team Lid 1**: Niemand\n**Team Lid 2**: Niemand\n\nTeam hoppen is verboden en levert een ban op van de Economie game!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
                else:
                    await ctx.send(f"Je zit al in een team. Verlaat je huidige team om een team te kunnen aanmaken. `{prefix}team verlaat`")
            elif setting == "verwijder" or setting == "delete":
                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE team_leader = {ctx.author.id}")
                teams_leaderdata = maxergdb_cursor.fetchone()

                if teams_leaderdata is None:
                    await ctx.send(f"Je bent niet de eigenaar van je team. Wil je je team verlaten? Gebruik dan `{prefix}team verlaat`")
                else:
                    maxergdb_cursor.execute(f"DELETE FROM maxerg_teams WHERE team_leader = {ctx.author.id}")
                    db_maxerg.commit()

                    em = discord.Embed(
                        title="Team verwijderd!",
                        description=f"Je team is succesvol verwijderd!\n\nTeam hoppen is verboden en levert een ban op van de Economie game!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
            elif setting == "leave" or setting == "verlaat":
                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE team_leader = {ctx.author.id} OR member_one = {ctx.author.id} OR member_two = {ctx.author.id}")
                teams_userdata = maxergdb_cursor.fetchone()

                if teams_userdata is None:
                    await ctx.send(f"Je zit nog niet in een team! Wil je een team joinen, vraag dan aan de leider van een team om je te inviten. Gebruik: `{prefix}team invite <naam>`")
                else:
                    leader = teams_userdata[0]
                    lid1 = teams_userdata[1]
                    lid2 = teams_userdata[2]

                    if leader == ctx.author.id:
                        await ctx.send(f"Je bent de eigenaar van je team. Wil je je team verwijderen? Gebruik dan `{prefix}team verwijder`")
                    elif lid1 == ctx.author.id:
                        maxergdb_cursor.execute(f"UPDATE maxerg_teams SET member_one = 0 WHERE team_leader = {leader}")
                    elif lid2 == ctx.author.id:
                        maxergdb_cursor.execute(f"UPDATE maxerg_teams SET member_two = 0 WHERE team_leader = {leader}")
                    db_maxerg.commit()

                    em = discord.Embed(
                        title="Team verlaten!",
                        description=f"Je hebt je team succesvol verlaten!\n\nTeam hoppen is verboden en levert een ban op van de Economie game!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
            elif setting == "remove":
                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE team_leader = {ctx.author.id}")
                teams_data = maxergdb_cursor.fetchone()

                team_leader = teams_data[0]
                team_member1 = teams_data[1]
                team_member2 = teams_data[2]

                if ctx.author.id != team_leader:
                    await ctx.send(f"Je bent niet de eigenaar van dit team.")
                else:
                    if member.id == team_member1:
                        maxergdb_cursor.execute(f"UPDATE maxerg_teams SET member_one = 0 WHERE team_leader = {ctx.author.id}")
                        await member.send(f"Je bent verwijderd van je team in **{ctx.guild}** door **{ctx.author}**")

                        em = discord.Embed(
                            title="Teamlid verwijderd!",
                            description=f"Je hebt succesvol een teamlid verwijderd!\n\nTeam hoppen is verboden en levert een ban op van de Economie game!",
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        em.set_footer(text=footer)
                        await ctx.send(embed=em)
                    elif member.id == team_member2:
                        maxergdb_cursor.execute(f"UPDATE maxerg_teams SET member_two = 0 WHERE team_leader = {ctx.author.id}")
                        await member.send(f"Je bent verwijderd van je team in **{ctx.guild}** door **{ctx.author}**")

                        em = discord.Embed(
                            title="Teamlid verwijderd!",
                            description=f"Je hebt succesvol een teamlid verwijderd!\n\nTeam hoppen is verboden en levert een ban op van de Economie game!",
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        em.set_footer(text=footer)
                        await ctx.send(embed=em)
                    else:
                        await ctx.send(f"Deze gebruiker zit niet in je team. Wil je deze gebruiker inviten tot je team? Gebruik dan `{prefix}team invite <naam>`")
                    db_maxerg.commit()
            elif setting == "invite":
                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE team_leader = {ctx.author.id}")
                teams_leaderdata = maxergdb_cursor.fetchone()

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE member_one = {member.id} OR member_two = {member.id}")
                teams_memberdata = maxergdb_cursor.fetchone()

                if teams_leaderdata is None:
                    await ctx.send(f"Je bent niet de eigenaar van een team. Wil je je team verlaten? Gebruik dan `{prefix}team verlaat`")
                elif teams_memberdata is not None:
                    await ctx.send(f"Deze gebruiker zit al bij een team.")
                else:
                    em = discord.Embed(
                        title="Team Invite!",
                        description=f"Wachten op antwoord van {member.mention}...\n"
                                    f"Type `JA` om de invite te accepteren! De Invite is 90 seconden geldig!\n\n"
                                    f"Team hoppen is verboden en levert een ban op van de Economie game!",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    em.set_footer(text=footer)
                    change_em = await ctx.send(f"{member.mention}", embed=em)

                    def check(message):
                        return message.author == member and message.channel == ctx.channel and message.content.lower() == "ja"

                    try:
                        await self.client.wait_for('message', check=check, timeout=90)

                        if teams_leaderdata[1] == 0:
                            maxergdb_cursor.execute(f"UPDATE maxerg_teams SET member_one = {member.id} WHERE team_leader = {ctx.author.id}")
                        else:
                            maxergdb_cursor.execute(f"UPDATE maxerg_teams SET member_two = {member.id} WHERE team_leader = {ctx.author.id}")
                        db_maxerg.commit()

                        em = discord.Embed(
                            title="Team Invite!",
                            description=f"{member.mention} zit nu in het team.",
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        em.set_footer(text=footer)
                        await change_em.edit(embed=em)
                    except asyncio.TimeoutError:
                        em = discord.Embed(
                            title="Team Invite!",
                            description="Geen reactie gekregen. Probeer het opnieuw.",
                            color=embedcolor,
                            timestamp=datetime.datetime.utcnow()
                        )
                        em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        em.set_footer(text=footer)
                        await change_em.edit(embed=em)
            elif setting == "list":
                if member is None:
                    member = ctx.author

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_teams WHERE team_leader = {member.id} OR member_one = {member.id} OR member_two = {member.id}")
                teams_data = maxergdb_cursor.fetchone()

                if teams_data is not None:
                    team_leader = teams_data[0]
                    team_member1 = teams_data[1]
                    team_member2 = teams_data[2]

                    try:
                        if team_member1 != 0:
                            lid1 = self.client.get_user(team_member1)
                            lid1 = lid1.mention
                        else:
                            lid1 = "Niemand"
                    except AttributeError:
                        lid1 = team_member1

                    try:
                        if team_member2 != 0:
                            lid2 = self.client.get_user(team_member2)
                            lid2 = lid2.mention
                        else:
                            lid2 = "Niemand"
                    except AttributeError:
                        lid2 = team_member2

                    try:
                        leider = self.client.get_user(team_leader)
                        leider = leider.mention
                    except AttributeError:
                        leider = team_leader

                    em = discord.Embed(
                        title="Team Info",
                        description=f"**Team Leider:** {leider}\n**Team Lid 1**: {lid1}\n**Team Lid 2**: {lid2}",
                        color=embedcolor,
                        timestamp=datetime.datetime.utcnow()
                    )
                    em.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    em.set_footer(text=footer)
                    await ctx.send(embed=em)
                else:
                    await ctx.send(f"Je zit niet in een team.")
            else:
                await ctx.send(f"Ongeldige argumenten! Probeer het opnieuw!")
            db_maxerg.close()
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoTeam(client))
