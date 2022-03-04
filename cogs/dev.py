import discord, sys, traceback, typing, os, asyncio
from discord.ext import commands
from io import StringIO
from typing import Optional

from backend.tools import *
from backend.items import items as all_items

from database.main import *


def is_dev(ctx): return ctx.author.id == 470866478720090114


class Developer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	def get_user(self, id):
		if str(id) not in fetch_users(): User(ID=str(id)).save()
		return User.find(User.ID == str(id)).first()

	def get_game(self, game_id : str):
		return Game.find(Game.ID == game_id).first()
	
#	@commands.command()
#	@commands.is_owner()
#	async def dm(self, ctx, member: discord.User, message: str, embeded: Optional[bool] = False):
#		kwargs = {'content': f"{message}\n\nSupport Server: <{support_server_link}>"} if not (embeded) else {'embed': discord.Embed(title="Connect 4", description=f"{message}\n\n{support_server}")}
#		await member.send(**kwargs)
	

	@commands.command(aliases=['t'])
	@commands.is_owner()
	async def talk(self, ctx, msg, evaluate : Optional[bool] = False, embeded : Optional[bool] = False):
		try: msg = eval(msg) if (evaluate) else msg
		except Exception as e: await ctx.send(f"INPUT:\n```py\n{msg}\n```\nOUTPUT:\n```bash\n{e}\n```"); return

		if not (embeded): await ctx.send(msg); return

		embed = discord.Embed(description=msg, color=Color.default)
		await ctx.send(embed=embed)


	@commands.command(aliases=['cu'])
	@commands.is_owner()
	async def create_user(self, ctx, member : discord.Member):
		user = User(ID=str(member.id)).save()
		await ctx.send(user, delete_after=15)


	@commands.command(help="Evaluates Python code.", aliases=['python', 'eval', 'ev'])
	@commands.is_owner()
	async def py(self, ctx, unformatted : typing.Optional[bool], *, cmd):
		try: await ctx.message.delete()
		except: pass

		old_stdout = sys.stdout
		redirected_output = sys.stdout = StringIO()
		
		try:
			exec(str(cmd))
		
		except Exception as e:
			traceback.print_stack(file=sys.stdout)
			print(sys.exc_info())
		sys.stdout = old_stdout
		
		if (unformatted):
			msg = str(redirected_output.getvalue())
			msg = [await ctx.send(msg[i:i+2000]) for i in range(0, len(msg), 2000)]
		
		else:
			msg = str(redirected_output.getvalue())
			
			for i in range(0, len(msg), 2048):

				embed = discord.Embed(description=f"Input:\n```py\n{cmd}\n```\nOutput:\n```bash\n{msg[i:i+2000]}\n```")
				await ctx.send(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def load(self, ctx, cog : Optional[str] = None):
		if not (cog):
			for cog in os.listdir("cogs"):
				if not (cog.endswith(".py")) or (cog.startswith("dev")): continue

				try: self.bot.load_extension(f"cogs.{cog[:-3]}")
				except Exception as e: await ctx.author.send(f"[Main]: Failed to load '{cog[:-3]}': {e}")
				else: await ctx.send(f"[{cog[:-3]}]: Loaded..")

			return

		try: self.bot.load_extension(f"cogs.{cog}")
		except Exception as e: await ctx.author.send(f"[Main]: Failed to load '{cog}': {e}")
		else: await ctx.send(f"[{cog}]: Loaded..")

	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, cog : Optional[str] = None):
		if not (cog):
			for cog in os.listdir("cogs"):
				if not (cog.endswith(".py")) or (cog.startswith("dev")): continue

				try: self.bot.unload_extension(f"cogs.{cog[:-3]}")
				except Exception as e: await ctx.author.send(f"[Main]: Failed to unload '{cog[:-3]}': {e}")
				else: await ctx.send(f"[{cog[:-3]}]: Unloaded..")

			return

		try: self.bot.unload_extension(f"cogs.{cog}")
		except Exception as e: await ctx.author.send(f"[Main]: Failed to unload '{cog}': {e}")
		else: await ctx.send(f"[{cog}]: Unloaded..")

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, cog : Optional[str] = None):
		if not (cog):
			for cog in os.listdir("cogs"):
				if not (cog.endswith(".py")): continue

				try: self.bot.reload_extension(f"cogs.{cog[:-3]}")
				except Exception as e: await ctx.author.send(f"[Main]: Failed to reload '{cog[:-3]}': {e}")
				else: await ctx.send(f"[{cog[:-3]}]: Reloaded..")

			return

		try: self.bot.reload_extension(f"cogs.{cog}")
		except Exception as e: await ctx.author.send(f"[Main]: Failed to reload '{cog}': {e}")
		else: await ctx.send(f"[{cog}]: Reloaded..")


def setup(bot):
	bot.add_cog(Developer(bot))
