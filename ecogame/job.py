import datetime
import time
import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, password, database, embedcolor, footer, ecogame_channels


class EcoJob(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 259200, commands.BucketType.user)
    async def job(self, ctx, *, job=None):
        if str(ctx.channel) in ecogame_channels:
            job_list = ["mcdonalds werker", "leerkracht", "bouwvakker", "politie agent", "developer", "youtuber", "dokter", "advocaat", "rechter", "president"]
            job = job.lower()

            if job in job_list:
                db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
                maxergdb_cursor = db_maxerg.cursor()

                maxergdb_cursor.execute(f"SELECT * FROM maxerg_economie WHERE user_id = {ctx.author.id}")
                eco_data = maxergdb_cursor.fetchone()
                current_job = eco_data[5]
                prestige = eco_data[4]
                last_work = eco_data[6]
                risico = eco_data[7]

                embed_sturen = True
                if job == current_job:
                    await ctx.send("Je hebt deze job al...")
                    embed_sturen = False
                elif job == "bouwvakker" and prestige < 1:
                    await ctx.send(f"Deze job vereist minimaal prestige 1. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "politie agent" and prestige < 1:
                    await ctx.send(f"Deze job vereist minimaal prestige 1. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "developer" and prestige < 2:
                    await ctx.send(f"Deze job vereist minimaal prestige 2. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "youtuber" and prestige < 3:
                    await ctx.send(f"Deze job vereist minimaal prestige 3. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "dokter" and prestige < 4:
                    await ctx.send(f"Deze job vereist minimaal prestige 4. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "advocaat" and prestige < 5:
                    await ctx.send(f"Deze job vereist minimaal prestige 5. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "rechter" and prestige < 5:
                    await ctx.send(f"Deze job vereist minimaal prestige 5. Jij bent prestige `{prestige}`.")
                    embed_sturen = False
                elif job == "president" and prestige < 6:
                    await ctx.send(f"Deze job vereist minimaal prestige 6. Jij bent prestige `{prestige}`.")
                    embed_sturen = False

                if risico == 104:
                    tijd = datetime.datetime.utcnow()
                    tijd_ertussen = tijd - last_work
                    if tijd_ertussen.total_seconds() < 604800:
                        embed_sturen = False
                        tijd_over = round(last_work.timestamp()) + 604800
                        tijd_over = datetime.datetime.fromtimestamp(tijd_over).strftime("%d/%m/%Y om %Hu %Mm %Ss")

                        embed = discord.Embed(
                            title="Job Cooldown",
                            description=f"Je bent recent ontslagen van je job...\nWacht nog tot {tijd_over}",
                            color=embedcolor
                        )
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        embed.set_footer(text=footer)
                        await ctx.send(embed=embed)

                if embed_sturen:
                    current_time = datetime.datetime.utcnow()
                    last_work = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET job = %s WHERE user_id = %s", (job, ctx.author.id))
                    maxergdb_cursor.execute(f"UPDATE maxerg_economie SET last_work = %s WHERE user_id = %s", (last_work, ctx.author.id))
                    db_maxerg.commit()

                    embed = discord.Embed(
                        title="Job Veranderen",
                        description=f"Je job is veranderd van `{current_job}` naar `{job}`",
                        color=embedcolor
                    )
                    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)
                else:
                    ctx.command.reset_cooldown(ctx)
                db_maxerg.close()
            else:
                if job is None:
                    job = "NIET VERMELD"
                await ctx.send(f"Job '{job}' is niet geldig.")
                ctx.command.reset_cooldown(ctx)
        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Deze command werkt alleen in <#708055327958106164>.")

    @job.error
    async def job_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_limit = error.retry_after
            if cooldown_limit >= 86400:
                cooldown_limit -= 86400
                conversion = time.strftime("%#dd %#Hu %#Mm %#Ss", time.gmtime(cooldown_limit))
            elif 3600 <= cooldown_limit < 86400:
                conversion = time.strftime("%#Hu %#Mm %#Ss", time.gmtime(cooldown_limit))
            else:
                conversion = time.strftime("%#Mm %#Ss", time.gmtime(cooldown_limit))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=footer)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(EcoJob(client))
