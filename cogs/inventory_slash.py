from discord import Embed, ButtonStyle, Interaction, SelectOption
from discord.app_commands import command, guilds
from discord.ext.commands import Cog
from discord.ui import View, Select
from typing import Literal

from database import User, get_user, fetch_users
from utils import items as all_items, Color, test_server


class Disc_placements(Select):
	def __init__(self):
		options = [
			SelectOption(label="Primary", description="Set this disc as your primary disc."),
			SelectOption(label="Secondary", description="Set this disc as your secondary disc."),
		]

		super().__init__(placeholder="Primary or Secondary?", min_values=1, max_values=1, options=options)

	async def callback(self,interaction: Interaction):
		self.view.primary_disc = True if self.values[0].lower() == "primary" else False
		self.view.stop()


class Select_item(Select):
	def __init__(self, user, category):
		options = [SelectOption(label=item.replace('_', ' ').capitalize(), description="") for item in user.inventory[category] if not (all_items[category][item]['icon'] in [user.primary_disc, user.secondary_disc, user.background, user.embed_color])]

		super().__init__(placeholder="Select", min_values=1, max_values=1, options=options)

	async def callback(self, interaction: Interaction):
		self.view.value = self.values[0].lower().replace(' ', '_')
		self.view.stop()


class Inv_view(View):
	def __init__(self, user):
		super().__init__()
		self.value = None
		self.primary_disc = True
		self.user = user

	async def interaction_check(self, interaction: Interaction):
		return (str(interaction.user.id) == self.user.ID)


class Inv_slash(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	async def inventory(self, interaction: Interaction, category: Literal['Discs', 'Backgrounds']):
		user = get_user(interaction.user.id)
		category = category.lower().replace(' ', '_')

		items = ""
		for item in user.inventory[category]:
			items += f"{all_items[category][item]['icon']} - {item.replace('_', ' ').capitalize()}\n"

		embed = Embed(title="Inventory", description=items, color=Color.default)

		if (User(ID="0").inventory[category] == user.inventory[category]): await interaction.response.send_message(embed=embed, ephemeral=True); return
		
		view = Inv_view(user)
		view.add_item(Select_item(user, category))

		msg = await interaction.response.send_message(embed=embed, view=view)
		await view.wait()

		if view.value == None: await msg.delete(); return

		new_item = all_items[category][view.value]['icon']
		if (category == "discs"):
			view = Inv_view(user)
			view.add_item(Disc_placements())

			await msg.edit(content="Where?", embed=None, view=view)
			await view.wait()

			if (view.primary_disc):
				user.update(primary_disc=new_item)
				placement = "primary "

			else:
				user.update(secondary_disc=new_item)
				placement = "seconadry "

		if (category == "backgrounds"): user.update(background=new_item); print(18)

		await msg.delete()
		await interaction.response.send_message(f"{new_item} is your new `{placement}{category[:-1]}`", ephemeral=True)


def setup(bot):
	bot.add_cog(Inv_slash(bot))
