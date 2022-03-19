from discord import Status, Game, Intents
from discord.ext.commands import Bot
from os import environ, listdir
from dotenv import load_dotenv
from topgg import DBLClient
from random import randint

from database import User, fetch_users
from utils import test_server


class Connect4(Bot):
	def __init__(self):
		super().__init__(command_prefix="c-", case_sensitive=True, intents=Intents.default(), help_command=None, application_id=environ.get("APP_ID"))


	async def on_ready(self):
		await self.change_presence(status=Status.online, activity=Game("c-help"))
		print("running...")


	async def on_message(self, message):
		if (message.author.bot): return

		if self.user.mentioned_in(message):
			await message.channel.send("Type `/` and all of Connect 4's slash commands should appear.\nIf they don't then you have to reinvite the bot, you can do that by pressing on the bot and clicking " + '"Add To Server"' + " and selecting your server. If you're not the server owner please let them know.")
			return

		if str(message.author.id) in fetch_users():
			user = User.find(User.ID == str(message.author.id)).first()
			
			if user.exp >= (user.level * 4.231) * 100:
				user.update(exp=0)
				user.update(level=user.level + 1)
				
				coins = randint(100,1000)
				user.update(coins=user.coins + coins)
				
				await message.channel.send(f":tada: LEVEL UP! :tada:\nLevel: {user.level + 1}\nCoins: {user.coins + 1}")

		await self.process_commands(message)


	async def setup_hook(self):
		for file in listdir("cogs"):
			if file.endswith(".py"):
				try: await self.load_extension(f"cogs.{file[:-3]}")
				except Exception as e: print(f"[Main]: Failed to load '{file[:-3]}': {e}\n")
				else: print(f"[{file[:-3]}]: Loaded..\n")

		await self.tree.sync()
		await self.tree.sync(guild=test_server)


	# self.topggpy = DBLClient(self, environ.get("DBL_TOKEN"), autopost=True, post_shard_count=False)
	# async def on_autopost_success(self): print(f"Posted server count ({self.topggpy.guild_count}), shard count ({self.shard_count})")


if __name__ == ('__main__'):
	bot = Connect4()


	bot.remove_command("help")
	@bot.command(aliases=["?", "h"])
	async def help(ctx):
		await ctx.send("Type `/` and all of Connect 4's slash commands should appear.\nIf they don't then you have to reinvite the bot, you can do that by pressing on the bot and clicking " + '"Add To Server"' + " and selecting your server. If you're not the server owner please let them know.")


	load_dotenv('.env')
	bot.run(environ.get("TOKEN"))
