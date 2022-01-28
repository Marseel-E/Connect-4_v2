import discord
from discord import slash_utils as slash
from discord.ext import commands

from database.main import *


class Slash(slash.ApplicationCog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Slash(bot))
