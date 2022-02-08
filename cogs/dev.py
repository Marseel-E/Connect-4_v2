import discord, sys, traceback, typing, os, asyncio
from discord.ext import commands
from io import StringIO

from database.main import *


def is_dev(ctx): return ctx.author.id == 470866478720090114


class Developer(commands.Cog):
	def __init__(self, client):
		self.client = client


	def get_user(self, id):
		if str(id) not in fetch_users(): User(ID=str(id)).save()
		return User.find(User.ID == str(id)).first()

	def get_game(self, game_id : str):
		return Game.find(Game.ID == game_id).first()


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


def setup(client):
	client.add_cog(Developer(client))