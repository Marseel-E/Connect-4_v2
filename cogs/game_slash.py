from discord import Embed
import slash_util as slash
from typing import Optional, Literal

from database.main import *
from .play_slash import Backend


class Game_slash(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	# guild_id=879153063036858428
	@slash.slash_command()
	@slash.describe(leaderboard_type="Wins, loses, or Draws")
	async def leaderboard(self, ctx : slash.Context, leaderboard_type : Literal['wins', 'loses', 'draws'] = 'wins'):
		users = {}

		for user in [user for user in User.find(User.ID != '0').all()]:
			users[user.ID] = user.stats[leaderboard_type]

		users = sorted(users.items(), key=lambda x: x[1], reverse=True)

		description = ""
		for i in users:
			if users.index(i) >= 10: break

			user = await self.bot.fetch_user(i[0])
			
			if i[0] == str(ctx.author.id):
				user = f"**[{user}](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id})**"
			
			description += f"{users.index(i)+1}. **{user}** - `{i[1]}`\n"

		user = User.find(User.ID == str(ctx.author.id)).first() if str(ctx.author.id) in fetch_users() else User(ID=str(ctx.author.id), coins=1000).save()

		embed = Embed(title=f"Leaderboard - {leaderboard_type.capitalize()}", description=description, color=int("5261f8", 16))
		embed.set_footer(text=f"Your rank: {users.index((str(ctx.author.id), user.stats[leaderboard_type])) + 1}", icon_url=ctx.author.avatar.url)

		await ctx.send(embed=embed)


	# guild_id=879153063036858428
	@slash.slash_command()
	async def board(self, ctx : slash.Context):
		if str(ctx.author.id) not in fetch_users(): return

		user = User.find(User.ID == str(ctx.author.id)).first()

		if not user.playing: await ctx.send(f"{ctx.author.mention}, Your not playing.", ephemeral=True); return
		
		game = Game.find(Game.ID == user.ID).first()
		member = User.find(User.ID == game.players[1]).first()

		board = await Backend(game.ID).style_board()

		embed = Embed(title="Connect 4", description=f"**[Jump to original message to play]({game.message})**\n{board}", color = int(user.embed_color, 16))
		embed.set_footer(text=f"ID: {game.ID}")

		turn_user = await self.bot.fetch_user(int(game.turn))
		embed.add_field(name="Turn:", value=turn_user.mention, inline=False)
		
		await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
	bot.add_cog(Game_slash(bot))