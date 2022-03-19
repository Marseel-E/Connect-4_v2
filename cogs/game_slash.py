from typing import Optional, Literal, TYPE_CHECKING
from discord.app_commands import command, describe, guilds
from discord import Embed, Interaction
from discord.ext.commands import Cog

from database import get_user, fetch_users, User, Game
from uitls import test_server

if TYPE_CHECKING:
	from .play_slash import Backend


class Game_slash(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	@describe(leaderboard_type="Wins, loses, or Draws")
	async def leaderboard(self, interaction: Interaction, leaderboard_type: Literal['wins', 'loses', 'draws'] = 'wins'):
		users = {}
		for user in [user for user in User.find(User.ID != '0').all()]:
			users[user.ID] = user.stats[leaderboard_type]

		users = sorted(users.items(), key=lambda x: x[1], reverse=True)

		description = ""
		for i in users:
			if users.index(i) >= 10: break

			user = await self.bot.fetch_user(i[0])
			
			if i[0] == str(interaction.user.id):
				user = f"**[{user}](https://discord.com/channels/{interaction.guild.id}/{interaction.channel.id})**"
			
			description += f"{users.index(i)+1}. **{user}** - `{i[1]}`\n"

		user = get_user(interaction.user.id)

		embed = Embed(title=f"Leaderboard - {leaderboard_type.capitalize()}", description=description, color=int("5261f8", 16))
		embed.set_footer(text=f"Your rank: {users.index((str(interaction.user.id), user.stats[leaderboard_type])) + 1}", icon_url=interaction.user.avatar.url)

		await interaction.response.send_message(embed=embed)


	@command()
	@guilds(test_server)
	async def board(self, interaction: Interaction):
		if str(interaction.user.id) not in fetch_users(): return

		user = User.find(User.ID == str(interaction.user.id)).first()

		if not user.playing: await interaction.response.send_message(f"{interaction.user.mention}, Your not playing.", ephemeral=True); return
		
		game = Game.find(Game.ID == user.ID).first()
		member = User.find(User.ID == game.players[1]).first()

		board = await Backend(game.ID).style_board()

		embed = Embed(title="Connect 4", description=f"**[Jump to original message to play]({game.message})**\n{board}", color = int(user.embed_color, 16))
		embed.set_footer(text=f"ID: {game.ID}")

		turn_user = await self.bot.fetch_user(int(game.turn))
		embed.add_field(name="Turn:", value=turn_user.mention, inline=False)
		
		await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
	bot.add_cog(Game_slash(bot))