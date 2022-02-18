from slash_util import Cog, Modal, slash_command, Context, TextInput, TextInputStyle
from discord import Embed, TextChannel, Interaction, ButtonStyle
from discord.ui import View, button, Button
from asyncio import TimeoutError
from typing import Optional


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
		modal = Modal(title="Field maker", items=[
			TextInput(custom_id="name", label="Name", style=TextInputStyle.short, min_length=1, max_length=256),
			TextInput(custom_id="value", label="Value", style=TextInputStyle.paragraph, min_length=1, max_length=1024)
		])
		await interaction.response.send_modal(modal)

		try: modal_interaction = await modal.wait(timeout=300.0)
		except TimeoutError:
			await modal_interaction.response.send_message("You didn't respond in time.", ephemeral=True)
			await self.message.edit(view=None)
			self.stop()
		else: data = modal.response

		await modal_interaction.response.send_message("Adding field...", ephemeral=True)

		self.embed.add_field(name=data['name'], value=data['value'])
		button.label = "Add another field"

		await self.message.edit(embed=self.embed, view=self)
		self.timeout = 60.0


class Embed_maker(Cog):
	def __init__(self, bot):
		self.bot = bot


	@slash_command()
	async def embed(self, ctx : Context, channel : TextChannel = None):
		if (ctx.author.bot): return
		if not (ctx.author.guild_permissions.embed_links): 
			await ctx.send("You can't send embeds", ephemeral=True)
			return

		modal = Modal(title="Embed maker", items=[
			TextInput(custom_id="title", label="Title", style=TextInputStyle.short, max_length=256, required=False),
			TextInput(custom_id="description", label="Description", style=TextInputStyle.paragraph, max_length=4000, required=False),
			TextInput(custom_id="color", label="Color", style=TextInputStyle.short, min_length=6, max_length=6, placeholder="hex code", default_value="000000", required=False),
			TextInput(custom_id="footer", label="Footer", style=TextInputStyle.short, max_length=2048, required=False)
		])
		await ctx.send(modal=modal)

		try: interaction = await modal.wait(timeout=600.0)
		except TimeoutError:
			await interaction.response.send_message("You didn't respond in time.", ephemeral=True)
			return
		else: data = modal.response

		if (len(data['title']) + len(data['description']) + len(data['footer']) > 6000):
			await interaction.response.send_message("Your embed is too long.\nIts overall length cant exceed 6000 characters.", ephemeral=True)
			return

		await interaction.response.send_message("Preparing embed...", ephemeral=True)

		try: color = int(str(data['color']), 16)
		except ValueError: color = int("000000", 16)

		embed = Embed(title=data['title'], description=data['description'], color=color)
		if (data['footer']): embed.set_footer(text=data['footer'], icon_url=ctx.author.avatar)

		msg = await ctx.channel.send("Embed created!")

		view = Fields_view(ctx.author, embed, msg)
		await msg.edit(content="", embed=embed, view=view) if not (channel) else await channel.send(embed=embed, view=view)
		await view.wait()


def setup(bot):
	bot.add_cog(Embed_maker(bot))
