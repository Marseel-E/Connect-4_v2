from discord import ui, Embed, ButtonStyle, Member, SelectOption, Interaction
import slash_util as slash
import random

from database.main import *

class Backend:
	def __init__(self, game_id):
		self.game = Game.find(Game.ID == game_id).first()


	async def play_move(self, col):
		player = list(self.game.players).index(self.game.turn) + 1
		for row in reversed(range(len(self.game.board))):
			if (self.game.board[row][int(col)] == '0'): break

		new_board = list(self.game.board)

		new_row = new_board[row]
		new_row[int(col)] = str(player)
		
		new_board[row] = new_row

		return new_board


	async def win_check(self):
		board = self.game.board
		player = (self.game.players.index(self.game.turn) + 1)
		columns = 7; rows = 6

		# Horizontal
		for col in range(columns-3):
			for row in range(rows):
				if board[row][col] == str(player) and board[row][col+1] == str(player) and board[row][col+2] == str(player) and board[row][col+3] == str(player):
					board[row][col] = 'h'
					board[row][col+1] = 'h'
					board[row][col+2] = 'h'
					board[row][col+3] = 'h'
					
					return board

		# Vertical
		for col in range(columns):
			for row in range(rows-3):
				if board[row][col] == str(player) and board[row+1][col] == str(player) and board[row+2][col] == str(player) and board[row+3][col] == str(player):
					board[row][col] = 'v'
					board[row+1][col] = 'v'
					board[row+2][col] = 'v'
					board[row+3][col] = 'v'
					
					return board

		# Ascend
		for col in range(columns-3):
			for row in range(rows-3):
				if board[row][col] == str(player) and board[row+1][col+1] == str(player) and board[row+2][col+2] == str(player) and board[row+3][col+3] == str(player): 
					board[row][col] = 'a'
					board[row+1][col+1] = 'a'
					board[row+2][col+2] = 'a'
					board[row+3][col+3] = 'a'
					
					return board

		# Descend
		for col in range(columns-3):
			for row in range(3,rows):
				if board[row][col] == str(player) and board[row-1][col+1] == str(player) and board[row-2][col+2] == str(player) and board[row-3][col+3] == str(player):
					board[row][col] = 'd'
					board[row-1][col+1] = 'd'
					board[row-2][col+2] = 'd'
					board[row-3][col+3] = 'd'
					
					return board
		
		return False


	async def draw_check(self):
		for row in range(len(self.game.board)):
			for col in range(len(self.game.board[row])):
				if self.game.board[row][col] == '0': return False

		return True


	async def style_board(self):
		user = User.find(User.ID == self.game.players[0]).first()
		opponent = User.find(User.ID == self.game.players[1]).first()
		board = self.game.board
		new_board = ""
		user_disc = user.primary_disc
		opponent_disc = opponent.secondary_disc
		
		for row in range(len(board)):
			new_board += "\n"
			
			for col in range(len(board[row])):
				if board[row][col] == '0': new_board += f"{user.background} "
				if board[row][col] == '1': new_board += f"{user_disc} "
				if board[row][col] == '2': new_board += f"{opponent_disc} "
				if board[row][col] == 'v': new_board += "<:c4_vertical:855634500963926036> "
				if board[row][col] == 'h': new_board += "<:c4_horizontal:855634968750325791> "
				if board[row][col] == 'a': new_board += "<:c4_descending:855635141057576971> "
				if board[row][col] == 'd': new_board += "<:c4_ascending:855634992159522886> "

		return new_board


class Empty_view(ui.View):
	def __init__(self):
		super().__init__()


class Play_ask_view(ui.View):
	def __init__(self, author):
		super().__init__()
		self.value = None
		self.author = author

	async def interaction_check(self, interaction : Interaction):
		return (interaction.user.id == self.author.id)

	@ui.button(label="Accept", style=ButtonStyle.green)
	async def accept(self, button : ui.Button, interaction : Interaction):
		self.value = "accept"
		self.stop()

	@ui.button(label="Refuse", style=ButtonStyle.red)
	async def refuse(self, button : ui.Button, interaction : Interaction):
		self.value = "refuse"
		self.stop()

last_move = None

class Play_view(ui.View):
	def __init__(self, game):
		super().__init__()
		self.quit = False
		self.rechoose = False
		self.game = game

	async def interaction_check(self, interaction : Interaction):
		return (interaction.user.id == int(self.game.turn))

	@ui.select(placeholder="Play", min_values=1, max_values=1, options=[SelectOption(label=i, description=f"Row {i}") for i in range(1,8)])
	async def move_select(self, select : ui.Select, interaction : Interaction):
		move = int(select.values[0])-1

		if (self.game.board[0][move] != '0'): self.rechoose = True

		if not self.rechoose:
			new_board = await Backend(self.game.ID).play_move(move)

			if not (new_board):
				await interaction.response.send_message(":warning: An error occured, game will be considered a draw. :warning:")

				self.game.update(status="draw")
				self.quit = True

			self.game.update(board=new_board)

			global last_move
			last_move = move+1

		self.stop()

	@ui.button(label="Quit", style=ButtonStyle.red)
	async def quit(self, button : ui.Button, interaction : Interaction):
		self.quit = True

		self.game.update(status="win")

		if self.game.turn == self.game.players[0]: self.game.update(turn=self.game.players[1])
		else: self.game.update(turn=self.game.players[0])

		await interaction.response.send_message(f":warning: Player quit! :warning:")

		self.stop()


class Slash_play(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	# guild_id=879153063036858428
	@slash.slash_command()
	@slash.describe(member="Your opponent", bet="Your bet")
	async def play(self, ctx : slash.Context, member : Member, bet : int = 0):
		if (member.id == ctx.author.id):
			await ctx.send("No- just no.. you cant play with yourself.", ephemeral=True)
			return

		player = User.find(User.ID == str(ctx.author.id)).first()
		opponent = User.find(User.ID == str(member.id)).first()

		if (player.playing or opponent.playing):
			await ctx.send("You're playing another game", ephemeral=True)
			return

		bet = 0 if (bet < 0) else bet

		view = Play_ask_view(member)
		msg = await ctx.send(f"{member.mention}, `{ctx.author}` invited you to a game for {bet} :coin:", view=view)
		await view.wait()

		if view.value == "refuse":
			await msg.delete()
			await ctx.send(content=f"{ctx.author.mention}, `{member}` refused your invitation", ephemeral=True)
			return

		if view.value != "accept":
			await msg.edit(":warning: An error occured :warning:")
			return

		if (player.coins < bet) or (opponent.coins < bet):
			await msg.delete()
			await ctx.send(content="You or your opponent cant afford the bet", ephemeral=True)
			return

		if player.ID in fetch_games(): redis.delete(Game.find(Game.ID == player.ID).first().key())

		game = Game(ID=player.ID, players=[player.ID, opponent.ID], turn=player.ID, message=msg.jump_url).save()

		player.update(playing=True)
		player.update(coins=player.coins - bet)

		opponent.update(playing=True)
		opponent.update(coins=opponent.coins - bet)

		while not game.finished:
			pretty_board = await Backend(game.ID).style_board()

			embed = Embed(title="Connect 4", description=pretty_board, color=int(player.embed_color, 16))
			embed.set_footer(text=f"ID: {game.ID}")

			turn_user = await self.bot.fetch_user(int(game.turn)) 
			embed.add_field(name="Turn:", value=turn_user.mention, inline=False)

			while True:
				view = Play_view(game)
				global last_move
				await msg.edit(content=f"Last move: `{last_move}`", embed=embed, view=view)
				await view.wait()

				if not view.rechoose: break

				await ctx.send(":warning: Choose another move :warning:", ephemeral=True)

			if view.quit: break

			win_check = await Backend(game.ID).win_check()
			if (win_check != False):
				game.update(status="win")
				game.update(board=win_check)
				break

			draw_check = await Backend(game.ID).draw_check()
			if draw_check:
				game.update(status="draw")
				break

			if game.turn == game.players[0]: game.update(turn=game.players[1])
			else: game.update(turn=game.players[0])

		game.update(finished=True)

		player.update(playing=False)
		opponent.update(playing=False)

		if game.status == "win":
			amount = random.randint(1,100)
			loser = player if game.turn != player.ID else opponent
			new_stats = loser.stats
			new_stats['loses'] = (new_stats['loses'] + 1)
			loser.update(stats=new_stats)
			loser.update(exp=loser.exp + (amount * loser.level))

			winner = player if game.turn == player.ID else opponent
			winner.update(coins=winner.coins + (bet * 2))
			winner.update(exp=(winner.exp + (amount * winner.level)) * 2)

			new_stats = winner.stats
			new_stats['wins'] = (new_stats['wins'] + 1)
			winner.update(stats=new_stats)

			winner = await self.bot.fetch_user(int(winner.ID))
			win_msg = f":tada: {winner} won! :tada:"
		
		if game.status == "draw":
			amount = random.randint(1,100)
			player.update(coins=player.coins + bet)
			new_stats = player.stats
			new_stats['draws'] = (new_stats['draws'] + 1)
			player.update(stats=new_stats)
			player.update(exp=player.exp + (amount * player.level))

			opponent.update(coins=opponent.coins + bet)
			new_stats = opponent.stats
			new_stats['draws'] = (new_stats['draws'] + 1)
			opponent.update(stats=new_stats)
			opponent.update(exp=opponent.exp + (amount * opponent.level))

			win_msg = "draw"

		pretty_board = await Backend(game.ID).style_board()

		embed = Embed(title=win_msg, description=pretty_board, color=int("5261f8", 16))
		embed.set_footer(text=f"ID: {game.ID}")

		redis.delete(game.key())

		await msg.edit(content="", embed=embed, view=Empty_view())


def setup(bot):
	bot.add_cog(Slash_play(bot))
