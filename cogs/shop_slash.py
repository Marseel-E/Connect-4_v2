import slash_util as slash


class Shop_slash(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	@slash.slash_command(guild_id=843994109366501376)
	async def shop(self, ctx : slash.Context):
		await ctx.send("Soon...", ephemeral=True)


def setup(bot):
	bot.add_cog(Shop_slash(bot))