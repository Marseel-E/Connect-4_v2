import discord
from discord import slash, ButtonStyle, Interaction, ui, Button
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
        while True:
            global page
            view = HTP_view(ctx.author, page)
            await ctx.send(embed=embeds[page], view=view)
            await view.wait()

            if view.quit: break


def setup(bot):
    bot.add_cog(Slash(bot))
