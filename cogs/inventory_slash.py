from discord import Embed, ButtonStyle, Interaction, SelectOption
from discord.app_commands import command, guilds
from discord.ext.commands import Cog
from discord.ui import View, Select, button, Button
from typing import Literal

from database import User, get_user, fetch_users
from utils import items as all_items, Color, test_server, Paginator

class Disc_placement(View):
	def __init__(self, user, new_item):
		super().__init__()
		self.user = user
		self.new_item = new_item

		self.value = ""

	async def interaction_check(self, interaction: Interaction):
		return (str(interaction.user.id) == self.user.ID)


	@button(label="Primary", style=ButtonStyle.blurple)
	async def primary(self, button: Button, interaction: Interaction):
		self.user.update(primary_disc=self.new_item)
		self.value = "primary "

		self.stop()

	@button(label="Secondary", style=ButtonStyle.blurple)
	async def secondary(self, button: Button, interaction: Interaction):
		self.user.update(secondary_disc=self.new_item)
		self.value = "secondary "

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
			await interaction.edit_original_message(content="Where?", embed=None, view=view)
			await view.wait()

		if self.category == 'backgrounds': self.user.update(background=new_item)

		await interaction.delete_original_message()
		
		await interaction.response.send_message(f"{new_item} is your new `{view.value}{self.category[:-1]}`", ephemeral=True)

		await self.view.stop()


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




		# items = ""
		# for item in user.inventory[category]:
		# 	items += f"{all_items[category][item]['icon']} - {item.replace('_', ' ').capitalize()}\n"

		# embed = Embed(title="Inventory", description=items, color=Color.default)

		# if (User(ID="0").inventory[category] == user.inventory[category]): await interaction.response.send_message(embed=embed, ephemeral=True); return
		
		# view = Inv_view(user)
		# view.add_item(Select_item(user, category))

		# msg = await interaction.response.send_message(embed=embed, view=view)
		# await view.wait()

		# if view.value == None: await msg.delete(); return

		# new_item = all_items[category][view.value]['icon']
		# if (category == "discs"):
		# 	view = Inv_view(user)
		# 	view.add_item(Disc_placements())

		# 	await msg.edit(content="Where?", embed=None, view=view)
		# 	await view.wait()

		# 	if (view.primary_disc):
		# 		user.update(primary_disc=new_item)
		# 		placement = "primary "

		# 	else:
		# 		user.update(secondary_disc=new_item)
		# 		placement = "seconadry "

		# if (category == "backgrounds"): user.update(background=new_item); print(18)

		# await msg.delete()
		# await interaction.response.send_message(f"{new_item} is your new `{placement}{category[:-1]}`", ephemeral=True)


async def setup(bot):
	await bot.add_cog(Inv_slash(bot))
