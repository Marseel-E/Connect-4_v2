from discord import Interaction, Embed, ButtonStyle
from discord.ui import View, Button, button
from discord.app_commands import command, guilds
from discord.ext.commands import Cog

page = 1

from utils import test_server


class HTP_view(View):
	def __init__(self, author, page):
		super().__init__()
		self.quit = True
		self.author = author
		self.page = page

	async def interaction_check(self, interaction: Interaction):
		return interaction.user.id == self.author.id


	@button(label="<", style=ButtonStyle.gray)
	async def previous(self, button: Button, interaction: Interaction):
		global page
		
		if page > 1:
			page -= 1
			self.quit = False

		self.stop()

	@button(label=">", style=ButtonStyle.gray)
	async def next(self, button: Button, interaction: Interaction):
		global page

		if page < 3:
			page += 1
			self.quit = False

		self.stop()


class How_to_play(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command(name="how-to-play")
	@guilds(test_server)
	async def how_to_play(self, interaction: Interaction):
		embed_1 = Embed(title="How To Play - Basics", description="Connect 4 is a definite classic. Playing against an opponent, you try to be the first to place four discs in a row on the game board. While figuring out game winning strategy can sometimes be challenge, the game is simple enough to play. If you're gearing up for your first game, you'll get the hang of it in no time, especially if you're familiar with Tic-Tac-Toe.\nConnect 4 has 7 columns and 6 rows to choose from. You can choose any of the columns, depending on your strategy. When its your turn you pick a column to drop your piece in.", color=int("5261f8", 16))
		embed_1.add_field(name="You want to choose each move carefully because your opponent will have a turn after you.", value="Not only do they have a chance to thwart your strategy for four in row, your move can sometimes make it easier for them to get four of their checkers in a row.", inline=False)
		embed_1.add_field(name="If you have the first turn in the game:", value="your opponent will probably be responding to your moves and attempting to block you from getting four checkers in row.", inline=False)
		embed_1.add_field(name="If you have the second turn of the game:", value="you’ll likely be on the defensive, trying to keep your opponent from getting their checkers in row.", inline=False)
		embed_1.set_image(url="https://cdn.discordapp.com/attachments/846981732246880296/862915639227973632/SmartSelect_20210709-003839_Discord-Beta.jpg")
		
		embed_2 = Embed(title="How To Play - Goal", description="In order to win, a player must get four discs in their color in a row. Whoever does it first is the winner.", color=int("5261f8", 16))
		embed_2.add_field(name="There are three ways to get four checkers in a row:", value="horizontally, vertically, and diagonally.", inline=False)
		embed_2.set_image(url="https://cdn.discordapp.com/attachments/846981732246880296/862914973347872808/SmartSelect_20210709-003600_Discord-Beta.jpg")
		
		embed_3 = Embed(title="How To Play - Hints", description="If you are the first player to go in a game, your initial move can actually dictate the entire game. When you’re opening the game, the best move is to place your disc in the center column. By placing your disc in that slot, you made it much more difficult for your opponent to counter your moves so your chances of winning increase\nIf your opponent places their checker in the center column to open the game, don’t place yours in the same column so it’s on top of their checker. That doesn’t give you any strategic advantage. Instead, your best bet is to place your checker in the bottom row in one of the other columns and hope that your opponent makes a mistake.", color=int("5261f8", 16))
		embed_3.add_field(name="Placing the first checker in the middle column doesn’t guarantee a win.", value="You still have to avoid making mistakes along the way.", inline=False)
		embed_3.add_field(name="If you choose a column other than the middle for your first move:", value="it becomes easier for your opponent to force a tie.", inline=False)
		embed_3.add_field(name="If your opponent doesn’t place their checker in the center column with the first move of the game:", value="that should be your initial move when it’s your turn because the space offers the best advantage in the game.", inline=False)
		embed_3.set_image(url="https://cdn.discordapp.com/attachments/846981732246880296/862914134827466783/SmartSelect_20210709-002740_Discord-Beta.jpg")

		while True:
			global page
			page_embed = [embed_1, embed_2, embed_3][page-1]
			page_embed.set_footer(text=f"{page} / 3", icon_url=interaction.user.avatar.url)
			
			view = HTP_view(interaction.user, page)
			view.next.disabled = True if (page >= 3) else False
			view.previous.disabled = True if (page <= 1) else False

			await interaction.response.send_message(embed=page_embed, view=view, ephemeral=True)
			await view.wait()

			if view.quit: break


async def setup(bot):
	await bot.add_cog(How_to_play(bot))