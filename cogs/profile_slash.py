from discord import Interaction, User as DUser, Embed
from discord.app_commands import command, describe, guilds
from discord.ext.commands import Cog

from database import fetch_users, get_user
from utils import test_server


class Profile_slash(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	@describe(member="View another user's profile")
	async def profile(self, interaction: Interaction, member: DUser = None):
		discord_user = interaction.user or member
		
		if (member) and (str(discord_user.id) not in fetch_users()):
			await interaction.response.send_message('This user has no profile', ephemeral=True)
			return

		user = get_user(interaction.user.id)

		embed = Embed(color=int("5261f8", 16))
		embed.set_footer(text=f"Exp: {user.exp} / {round((user.level * 4.231) * 100)}")
		embed.set_thumbnail(url=discord_user.display_avatar)

		embed.add_field(name = ":beginner: Level", value = f"{user.level}", inline=False)
		embed.add_field(name = ":coin: Coins", value = f"{user.coins}", inline=False)

		wp = (user.stats['wins'] / sum(user.stats.values())) * 100 if (user.stats['wins'] > 0) else 0
		embed.add_field(name = ":bar_chart: Stats", value = f"Wins: {user.stats['wins']} (`{wp:.1f}%`) | Loses {user.stats['loses']} | Draws {user.stats['draws']}", inline=False)
		
		embed.add_field(name = ":art: Theme", value = f"Primary disc: {user.primary_disc} `({user.primary_disc.replace('_', ' ')})`\nSecondary disc: {user.secondary_disc} `({user.secondary_disc.replace('_', ' ')})`\nBackground: {user.background} `({user.background.replace('_', ' ')})`\nEmbed color: `{user.embed_color}`", inline=False)

		await interaction.response.send_message(embed=embed)


async def setup(bot):
	await bot.add_cog(Profile_slash(bot))