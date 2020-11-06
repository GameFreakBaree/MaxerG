import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels


class EcoInventory(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["inv", "invsee"])
    async def inventory(self, ctx, *, member: discord.Member = None):
        if str(ctx.channel) in ecogame_channels:
            if member is None:
                member = ctx.author

            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute(f"SELECT * FROM maxerg_inventory WHERE user_id = {member.id}")
            eco_data = maxergdb_cursor.fetchone()
            db_maxerg.close()

            vishengel_emote = slot_emote = geweer_emote = nitro_emote = hosting_emote = "<:error:725030739531268187>"

            if eco_data is not None:
                vishengel = eco_data[1]
                slot = eco_data[2]
                geweer = eco_data[3]
                nitro = eco_data[5]
                hosting = eco_data[6]

                if vishengel == 1:
                    vishengel_emote = "<:check:725030739543982240>"
                if slot == 1:
                    slot_emote = "<:check:725030739543982240>"
                if geweer == 1:
                    geweer_emote = "<:check:725030739543982240>"
                if nitro == 1:
                    nitro_emote = "<:check:725030739543982240>"
                if hosting == 1:
                    hosting_emote = "<:check:725030739543982240>"

            em = discord.Embed(
                title="Inventory",
                description=f"{vishengel_emote} **Vishengel**\n{slot_emote} **Slot**\n{geweer_emote} **Geweer**\n{nitro_emote} **Discord Nitro Classic**\n{hosting_emote} **Discord Bot Hosting**",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoInventory(client))
