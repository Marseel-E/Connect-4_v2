import discord
import slash_util as slash

from database.main import *


def fix(name): return name.replace('_', ' ') if name is not None else name

class Profile_slash(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	# guild_id=879153063036858428
	@slash.slash_command()
	@slash.describe(member="View another user's profile")
	async def profile(self, ctx : slash.Context, member : discord.User = None):
		try: await ctx.message.delete()
		except: pass

		discord_user = ctx.author if not member else member
		
		if str(discord_user.id) not in fetch_users():
			if member: await ctx.send('This user has no profile'); return
			else: User(ID=str(discord_user.id)).save()

		user = User.find(User.ID == str(discord_user.id)).first()

		embed = discord.Embed(color=int("5261f8", 16))
		embed.set_footer(text=f"Exp: {user.exp} / {round((user.level * 4.231) * 100)}")
		embed.set_thumbnail(url=discord_user.display_avatar)

		embed.add_field(name = ":beginner: Level", value = f"{user.level}", inline=False)
		embed.add_field(name = ":coin: Coins", value = f"{user.coins}", inline=False)

		wp = (user.stats['wins'] / sum(user.stats.values())) * 100 if user.stats['wins'] > 0 else 0
		embed.add_field(name = ":bar_chart: Stats", value = f"Wins: {user.stats['wins']} (`{wp:.1f}%`) | Loses {user.stats['loses']} | Draws {user.stats['draws']}", inline=False)
		
		embed.add_field(name = ":art: Theme", value = f"Primary disc: {user.primary_disc} `({user.primary_disc.replace('_', ' ')})`\nSecondary disc: {user.secondary_disc} `({user.secondary_disc.replace('_', ' ')})`\nBackground: {user.background} `({user.background.replace('_', ' ')})`\nEmbed color: `{user.embed_color}`", inline=False)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Profile_slash(bot))