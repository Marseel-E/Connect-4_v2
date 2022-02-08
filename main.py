import discord, os, random, typing
import slash_util as slash
from discord.ext import commands

from database.main import *

from dotenv import load_dotenv
load_dotenv('.env')


intents = discord.Intents.default()
intents.guilds=True
intents.members=True
intents.reactions=True

bot = slash.Bot(command_prefix=commands.when_mentioned_or('-'), case_sensitive=True, intents=intents)


@bot.event
async def on_ready():
    print("running...")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("connect-4.exe"))


@bot.event
async def on_message(message):
    if (message.author.bot): return

    if bot.user.mentioned_in(message): await message.channel.send("Type `/` and all of Connect 4's slash commands should appear.\nIf they don't then you have to reinvite the bot, you can do that by pressing on the bot and clicking " + '"Add To Server"'+ " and selecting your server. If you're not the server owner please let him know."); return
    users = fetch_users()
    if str(message.author.id) in users:
        user = User.find(User.ID == str(message.author.id)).first()
        
        if user.exp >= (user.level * 4.231) * 100:
            user.update(exp=0)
            user.update(level=user.level + 1)
            
            coins = random.randint(100,1000)
            user.update(coins=user.coins + coins)
            
            await message.channel.send(f":tada: LEVEL UP! :tada:\nLevel: {user.level + 1}\nCoins: {user.coins + 1}")

    await bot.process_commands(message)


if __name__ == ('__main__'):
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"[Main]: Failed to load '{file[:-3]}': {e}\n")
            else:
                print(f"[{file[:-3]}]: Loaded..\n")


bot.run(os.environ.get("TOKEN"))
