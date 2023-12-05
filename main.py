import discord
from discord.ext import commands
import os
import cogs.crawler


intents = discord.Intents.all()
intents.guilds = True

# GUILD_IDSが複数あるか
if os.getenv("GUILD_IDS").find(",") != -1:
    bot = commands.AutoShardedBot(
        intents=intents, debug_guilds=list(
            map(int, os.getenv("GUILD_IDS").split(",")))
    )
else:
    bot = commands.Bot(
        command_prefix="/", intents=intents, debug_guild=int(os.getenv("GUILD_IDS"))
    )

TOKEN = os.getenv(f"TOKEN")

path = "./cogs"


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond(content="BOT管理者限定コマンドです", ephemeral=True)
    else:
        raise error


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")
    
    # GUILD_IDSが複数あるか
    if os.getenv("GUILD_IDS").find(",") != -1:
        for guild_id in list(map(int, os.getenv("GUILD_IDS").split(","))):
            guild = bot.get_guild(guild_id)
            await cogs.crawler.Crawler().all_channel(guild)
    else:
        guild = bot.get_guild(int(os.getenv("GUILD_IDS")))
        await cogs.crawler.Crawler().all_channel(guild)
            



bot.run(TOKEN)
