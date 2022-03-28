from discord import Embed, ButtonStyle, Interaction, SelectOption
from discord.ui import View, Select, button, Button
from discord.app_commands import command, guilds
from discord.ext.commands import Cog
from paginator import Paginator
from typing import Literal

from database import User, get_user, fetch_users
from utils import items as all_items, Color, test_server

class Disc_placement(View):
	def __init__(self, user, new_item):
		super().__init__()
		self.user = user
		self.new_item = new_item

	async def interaction_check(self, interaction: Interaction):
		return (str(interaction.user.id) == self.user.ID)


	@button(label="Primary", style=ButtonStyle.blurple)
	async def primary(self, interaction: Interaction, button: Button):
		self.user.update(primary_disc=self.new_item)

		await interaction.response.send_message(f"{self.new_item} is your new `primary disc`", ephemeral=True)

		self.stop()

	@button(label="Secondary", style=ButtonStyle.blurple)
	async def secondary(self, interaction: Interaction, button: Button):
		self.user.update(secondary_disc=self.new_item)
		
		await interaction.response.send_message(f"{self.new_item} is your new `secondary disc`", ephemeral=True)

		self.stop()


class Select_item(Select):
	def __init__(self, user, category):
		self.user = user
		self.category = category

		options = [SelectOption(label=item.replace('_', ' ').capitalize(), description="") for item in user.inventory[category] if not (all_items[category][item]['icon'] in [user.primary_disc, user.secondary_disc, user.background, user.embed_color])]

		super().__init__(placeholder="Select", min_values=1, max_values=1, options=options)

	async def callback(self, interaction: Interaction):
		new_item = all_items[self.category][self.values[0].lower().replace(' ', '_')]['icon']

		if self.category == 'discs':
			view = Disc_placement(self.user, new_item)
			await interaction.response.send_message(content="Where?", view=view, ephemeral=True)
			await view.wait()

		if self.category == 'backgrounds':
			self.user.update(background=new_item)
			await interaction.response.send_message(f"{new_item} is your new `background`", ephemeral=True)

		self.view.stop()


class Inv_slash(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	async def inventory(self, interaction: Interaction, category: Literal['Discs', 'Backgrounds'] = 'Discs'):
		user = get_user(interaction.user.id)
		category = category.lower()


		pages = []
		for i, item in enumerate(user.inventory[category]):
			if (i == 0) or (i + 1 % 10 == 0):
				embed = Embed(title="Inventory", description="", color=Color.default)
				if i > 0: pages.append(embed)

			embed.description += f"{all_items[category][item]['icon']} - {item.replace('_', ' ').capitalize()}\n"

		if (embed not in pages) and (embed.description != ""): pages.append(embed)

		kwargs = {
			'interaction': interaction,
			'pages': pages
		}
		if not (User(ID="0").inventory[category] == user.inventory[category]): kwargs['custom_children'] = [Select_item(user, category)]

		await Paginator(**kwargs).start(True)


async def setup(bot):
	await bot.add_cog(Inv_slash(bot))
