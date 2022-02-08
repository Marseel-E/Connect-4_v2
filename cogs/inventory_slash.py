import slash_util as slash


class Inv_slash(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	@slash.slash_command()
	async def inventory(self, ctx : slash.Context):
		await ctx.send("Soon...", ephemeral=True)


def setup(bot):
	bot.add_cog(Inv_slash(bot))