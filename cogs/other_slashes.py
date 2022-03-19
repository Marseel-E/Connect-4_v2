from discord.app_commands import command, describe, guilds
from discord import Embed, Interaction
from discord.ext.commands import Cog

from database import fetch_users, User
from utils import default_bot, support_server, Color, test_server


class Other_slashes(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	@describe(hex_code="A hex code")
	async def color(self, interaction: Interaction, hex_code: str):
		embed = Embed(title=hex_code, color=int(hex_code, 16))
		await interaction.response.send_message(embed=embed, ephemeral=True)


	@command(guild=test_server)
	async def stats(self, interaction: Interaction):
		owner = await self.bot.fetch_user(470866478720090114)
		users = fetch_users()

		games = 0
		for user in users:
			user = User.find(User.ID == str(user)).first()
			games += sum(list(user.stats.values()))

		emojis = [f"<:{emoji.name}:{emoji.id}>" for emoji in self.bot.emojis]
		
		embed = Embed(title="Stats", description=self.bot.description, color=Color.default)
		embed.set_footer(text=f"Latency: {round(self.bot.latency)}ms")
		embed.set_thumbnail(url=self.bot.user.display_avatar)

		embed.add_field(name="Creator:", value=f"[{owner}](https://discord.com/users/{owner.id})", inline=False)
		embed.add_field(name="Guilds:", value=f"`{len(self.bot.guilds)}`", inline=False)
		embed.add_field(name="Users:", value=f"`{len(users)}`", inline=False)
		embed.add_field(name="Games:", value=f"`{games}`", inline=False)
		embed.add_field(name=f"Emojis: `({len(self.bot.emojis)})`", value=''.join(emojis[:30]), inline=False)

		await interaction.response.send_message(embed=embed, ephemeral=True)


	@command(name="bug-report", guild=test_server)
	@describe(description="A brief description of the problem")
	async def bug_report(self, interaction: Interaction, description: str):
		embed = Embed(title=":warning: Bug :warning:", description=description, color=Color.red)
		embed.set_footer(text=f"ID: {interaction.user.id}")

		channel = await self.bot.fetch_channel(855139711554289674)
		await channel.send(embed=embed)
		
		embed = Embed(description=f"Thanks for reaching out, Your report has been sent.\nPlease be patient while waiting for a response from our support team.\nVisit our {support_server} for urgent help.", color=Color.green)
		
		await interaction.response.send_message(embed=embed, ephemeral=True)


	@command(guild=test_server)
	async def permissions(self, interaction: Interaction):
		if not (True in [role.permissions.manage_guild for role in interaction.user.roles]):
			await interaction.response.send_message(":warning: `manage_guild` permission is required for this command", ephemeral=True)
			return

		required = ""
		optional = ""
		other = ""
		required_amount = 0
		optional_amount = 0
		other_amount = 0

		required_perms = ["add_reactions", "embed_links", "external_emojis", "read_messages", "send_messages"]
		optional_perms = ["attach_files", "change_nickname", "create_instant_invite", "manage_messages", "read_message_history"]

		perms = list(interaction.guild.me.guild_permissions)

		for perm in perms:
			if (perm[1]):
				if perm[0] in required_perms:
					required += f"`{perm[0]}`\n"
					required_amount += 1
				elif perm[0] in optional_perms:
					optional += f"`{perm[0]}`\n"
					optional_amount += 1
				else:
					other += f"`{perm[0]}`\n"
					other_amount += 1
			else:
				if perm[0] in required_perms: required += f":warning: `{perm[0]}` **(Missing)**\n"
				elif perm[0] in optional_perms: optional += f"`{perm[0]}` **(Missing)**\n"
				else: pass

		embed = Embed(title="Permissions", color=Color.default)

		embed.add_field(name=f":white_check_mark: Required: `({required_amount}/{len(required_perms)})`", value=required, inline=False)
		embed.add_field(name=f":ballot_box_with_check: Optional: `({optional_amount}/{len(optional_perms)})`", value=optional, inline=False)

		if (other != ""): embed.add_field(name=f":no_entry_sign: Not required: `({other_amount})`", value=other, inline=False)

		await interaction.response.send_message(embed=embed, ephemeral=True)


	@command(guild=test_server)
	async def invite(self, interaction: Interaction):
		embed = Embed(title="Links", description=f"**{default_bot}**\n**{support_server}**", color=Color.default)
		await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
	bot.add_cog(Other_slashes(bot))