import discord
from discord import slash, ButtonStyle, Interaction, ui, Button, Embed
from discord.ext import commands

from database.main import *


page = 1

class HTP_view(ui.View):
    def __init__(self, author, page):
        super().__init__()
        self.quit = True
        self.author = author
        self.page = page

    async def interaction_check(self, interaction : Interaction):
        return interaction.user.id == self.author.id


    @ui.Button(label="<", style=ButtonStyle.gray)
    async def previous(self, button : Button, interaction : Interaction):
        global page

        if page > 1:
            page -= 1
            self.quit = False

        self.stop()

    @ui.Button(label=">", style=ButtonStyle.gray)
    async def next(self, button : Button, interaction : Interaction):
        global page

        if page < 3:
            page += 1
            self.quit = False

        self.stop()

class Slash(slash.ApplicationCog):
    def __init__(self, bot):
        self.bot = bot


    @slash.command(name=how-to-play)
    @slash.describe("How to play Connect 4")
    async def how_to_play(self, ctx : slash.Context):
        embed_1 = Embed(title="How To Play - Basics", description="Connect 4 is a definite classic. Playing against an opponent, you try to be the first to place four discs in a row on the game board. While figuring out game winning strategy can sometimes be challenge, the game is simple enough to play. If you're gearing up for your first game, you'll get the hang of it in no time, especially if you're familiar with Tic-Tac-Toe.\nConnect 4 has 7 columns and 6 rows to choose from. You can choose any of the columns, depending on your strategy. When its your turn you pick a column to drop your piece in.", color=int("5261f8", 16))
        embed_2 = Embed(title="How To Play - Goal", description=In order to win, a player must get four discs in their color in a row. Whoever does it first is the winner.", color=int("5261f8", 16))
        embed_3 = Embed(title="How To Play - Hints", description="If you are the first player to go in a game, your initial move can actually dictate the entire game. When you’re opening the game, the best move is to place your disc in the center column. By placing your disc in that slot, you made it much more difficult for your opponent to counter your moves so your chances of winning increase\nIf your opponent places their checker in the center column to open the game, don’t place yours in the same column so it’s on top of their checker. That doesn’t give you any strategic advantage. Instead, your best bet is to place your checker in the bottom row in one of the other columns and hope that your opponent makes a mistake.", color=int("5261f8", 16))

        # embed_1 = ["You want to choose each move carefully because your opponent will have a turn after you.\s Not only do they have a chance to thwart your strategy for four in row, your move can sometimes make it easier for them to get four of their checkers in a row.\s False", "If you have the first turn in the game:\s your opponent will probably be responding to your moves and attempting to block you from getting four checkers in row.\s False", "If you have the second turn of the game:\s you’ll likely be on the defensive, trying to keep your opponent from getting their checkers in row.\s False"]
        embed_1.set_image(url="https://cdn.discordapp.com/attachments/846981732246880296/862915639227973632/SmartSelect_20210709-003839_Discord-Beta.jpg")
        
        # embed_2 = ["There are three ways to get four checkers in a row:\s horizontally, vertically, and diagonally.\s False"]  
        embed_2.set_image(url="https://cdn.discordapp.com/attachments/846981732246880296/862914973347872808/SmartSelect_20210709-003600_Discord-Beta.jpg")
        
        # embed_3 = ["Placing the first checker in the middle column doesn’t guarantee a win.\s You still have to avoid making mistakes along the way.\s False", "If you choose a column other than the middle for your first move:\s it becomes easier for your opponent to force a tie.\s False", "If your opponent doesn’t place their checker in the center column with the first move of the game:\s that should be your initial move when it’s your turn because the space offers the best advantage in the game.\s False"]  
        embed_3.set_image(url="https://cdn.discordapp.com/attachments/846981732246880296/862914134827466783/SmartSelect_20210709-002740_Discord-Beta.jpg")

        while True:
            global page
            view = HTP_view(ctx.author, page)
            await ctx.send(embed=[embed_1, embed_2, embed_3][page], view=view)
            await view.wait()

            if view.quit: break


def setup(bot):
    bot.add_cog(Slash(bot))
