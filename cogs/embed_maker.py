from discord import Embed, TextChannel, Interaction, ButtonStyle, TextStyle
from discord.ui import View, button, Button, Modal, TextInput
from discord.app_commands import command, guilds
from discord.ext.commands import Cog
from asyncio import TimeoutError
from typing import Optional

from utils import test_server


class field_modal(Modal, title="Field Maker"):
	name = TextInput(label="Name", min_length=1, max_length=256)
	value = TextInput(label="Value", min_length=1, max_length=1024, style=TextStyle.paragraph)


class Fields_view(View):
	def __init__(self, author, embed, message):
		super().__init__()
		self.author = author
		self.embed = embed
		self.message = message

		self.timeout = 60.0

	async def interaction_check(self, interaction : Interaction):
		return(interaction.user.id == self.author.id)

	async def on_timeout(self):
		await self.message.edit(view=None)
		self.stop()


	@button(label="Add field", style=ButtonStyle.blurple)
	async def add_field(self, button : Button, interaction : Interaction):
		modal = field_modal()
		await interaction.response.send_modal(modal)

		try: modal_interaction = await modal.wait()
		except TimeoutError:
			await modal_interaction.response.send_message("You didn't respond in time.", ephemeral=True)
			await self.message.edit(view=None)
			self.stop()

		await modal_interaction.response.send_message("Adding field...", ephemeral=True)

		self.embed.add_field(name=modal.name, value=modal.value)
		button.label = "Add another field"

		await self.message.edit(embed=self.embed, view=self)
		self.timeout = 60.0


class embed_modal(Modal, title="Embed Maker"):
	title = TextInput(label="Title", max_length=256, required=True)
	description = TextInput(label="Description", max_length=4000, style=TextStyle.paragraph)
	color = TextInput(label="Color", min_length=6, max_length=6, placeholder="hex code", default="000000")
	footer = TextInput(label="Footer", max_length=2048)


class Embed_maker(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	async def embed(self, interaction: Interaction, channel: TextChannel = None):
		if (interaction.user.bot): return
		if not (interaction.user.guild_permissions.embed_links): 
			await interaction.response.send_message("You can't send embeds", ephemeral=True)
			return

		modal = embed_modal()
		await interaction.response.send_modal(modal=modal)

		try: interaction = await modal.wait()
		except TimeoutError:
			await interaction.response.send_message("You didn't respond in time.", ephemeral=True)
			return

		if (len(modal.title) + len(modal.description) + len(modal.footer) > 6000):
			await interaction.response.send_message("Your embed is too long.\nIts overall length cant exceed 6000 characters.", ephemeral=True)
			return

		await interaction.response.send_message("Preparing embed...", ephemeral=True)

		try: color = int(str(modal.color), 16)
		except ValueError: color = int("000000", 16)

		embed = Embed(title=modal.title, description=modal.description, color=color)
		if (modal.footer): embed.set_footer(text=modal.footer, icon_url=interaction.user.avatar)

		msg = await interaction.channel.send("Embed created!")

		view = Fields_view(interaction.user, embed, msg)
		await msg.edit(content="", embed=embed, view=view) if not (channel) else await channel.send(embed=embed, view=view)
		await view.wait()


async def setup(bot):
	await bot.add_cog(Embed_maker(bot))
