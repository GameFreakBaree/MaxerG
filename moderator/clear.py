import time
import discord
import datetime
import json
import mysql.connector
from discord.ext import commands
from discord.ext.commands import MissingPermissions

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


class Clear(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["purge", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        if amount == 0:
            await ctx.channel.purge(limit=1)
            delete_message = await ctx.send(
                "Je moet een waarde groter dan 0 meegeven aan de command (bv: `!clear 5`).")
            time.sleep(3)
            await delete_message.delete()
        elif amount > 125:
            await ctx.channel.purge(limit=1)
            delete_message = await ctx.send("Je moet een waarde kleiner dan 125 gebruiken.")
            time.sleep(3)
            await delete_message.delete()
        else:
            await ctx.channel.purge(limit=amount + 1)
            if amount == 1:
                delete_message = await ctx.send(f"{amount} bericht is verwijderd!")
                time.sleep(3)
                await delete_message.delete()
            else:
                delete_message = await ctx.send(f"{amount} berichten zijn verwijderd!")
                time.sleep(3)
                await delete_message.delete()

            db_maxerg.commit()
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            log_channel = self.client.get_channel(742715965128704030)
            clear_embed = discord.Embed(
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            clear_embed.add_field(name="Moderator", value=f"**Naam:**\t{ctx.author.mention}\n**ID:**\t{ctx.author.id}",
                                  inline=True)
            clear_embed.add_field(name="Aantal Berichten", value=f"{amount}", inline=True)
            clear_embed.add_field(name="Channel", value=f"{ctx.channel.mention}", inline=True)
            clear_embed.set_author(name=f"[CLEAR] {ctx.author}", icon_url=ctx.author.avatar_url)
            clear_embed.set_footer(text=embed_footer[0])
            await log_channel.send(embed=clear_embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return


def setup(client):
    client.add_cog(Clear(client))
