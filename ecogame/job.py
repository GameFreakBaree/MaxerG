import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels


class EcoJob(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def job(self, ctx, *, job=None):
        if str(ctx.channel) in ecogame_channels:
            job_list = ["mcdonalds werker", "leerkracht", "bouwvakker", "politie agent", "boekhouder", "developer", "youtuber", "dokter", "advocaat", "rechter", "ceo", "minister", "president"]
            job = job.lower()

            if job in job_list:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                eco_data = maxergdb_cursor.fetchone()
                current_job = eco_data[5]
                prestige = eco_data[4]

                embed_sturen = True
                if job == current_job:
                    await ctx.send("Je hebt deze job al...")
                    embed_sturen = False
                elif job == "leerkracht" and prestige < 1:
                    await ctx.send(f"Deze job vereist minimaal prestige 1. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "bouwvakker" and prestige < 2:
                    await ctx.send(f"Deze job vereist minimaal prestige 2. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "politie agent" and prestige < 3:
                    await ctx.send(f"Deze job vereist minimaal prestige 3. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "boekhouder" and prestige < 4:
                    await ctx.send(f"Deze job vereist minimaal prestige 4. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "developer" and prestige < 5:
                    await ctx.send(f"Deze job vereist minimaal prestige 5. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "youtuber" and prestige < 6:
                    await ctx.send(f"Deze job vereist minimaal prestige 6. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "dokter" and prestige < 7:
                    await ctx.send(f"Deze job vereist minimaal prestige 7. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "advocaat" and prestige < 8:
                    await ctx.send(f"Deze job vereist minimaal prestige 8. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "rechter" and prestige < 9:
                    await ctx.send(f"Deze job vereist minimaal prestige 9. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "ceo" and prestige < 10:
                    await ctx.send(f"Deze job vereist minimaal prestige 10. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "minister" and prestige < 11:
                    await ctx.send(f"Deze job vereist minimaal prestige 11. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "president" and prestige < 12:
                    await ctx.send(f"Deze job vereist minimaal prestige 12. Jij bent prestige `{prestige}`.")
                    embed_sturen = False

                if embed_sturen:
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET job = %s WHERE user_id = %s", (job, ctx.author.id))
                    db_maxerg.commit()

                    embed = discord.Embed(
                        title="Job Veranderen",
                        description=f"Je job is veranderd van `{current_job}` naar `{job}`",
                        color=embedcolor
                    )
                    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)
                db_maxerg.close()
            else:
                if job is None:
                    job = "NIET VERMELD"
                await ctx.send(f"Job '{job}' is niet geldig.")
        else:
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")


def setup(client):
    client.add_cog(EcoJob(client))
