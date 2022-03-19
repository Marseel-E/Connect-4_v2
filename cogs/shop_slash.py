from discord import Embed, Interaction, SelectOption
from discord.app_commands import command, guilds
from discord.ext.commands import Cog
from discord.ui import View, Select
from typing import Literal

from database import User, fetch_users
from utils import items as all_items, Color, test_server


class Buy_dropdown(Select):
	def __init__(self, user, category):
		self.user = user
		self.category = category

		options = [SelectOption(label=key.replace('_', ' ').capitalize(), description=f"{value['price']}") for key, value in all_items[self.category].items() if ((value['price'] <= self.user.coins) and (value['price'] > 0))]

		super().__init__(placeholder="Buy", min_values=1, max_values=1, options=options)

	async def callback(self, interaction : Interaction):
		value = self.values[0].lower().replace(' ', '_')
		item = all_items[self.category][value]

		new_inventory = self.user.inventory
		new_inventory[self.category].append(value)

		assert new_inventory is not None
		self.user.update(inventory=new_inventory)
		self.user.update(coins=self.user.coins - item['price'])
		
		await interaction.response.send_message(f"Purchased {item['icon']} `{value}` for {item['price']} :coin:", ephemeral=True)
		self.view.stop()


class Shop_view(View):
	def __init__(self, user, category):
		super().__init__()
		self.user = user

		self.add_item(Buy_dropdown(self.user, category))

	async def interaction_check(self, interaction : Interaction):
		return (str(interaction.user.id) == self.user.ID)


class Shop_slash(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command()
	@guilds(test_server)
	async def shop(self, interaction: Interaction, category: Literal['Discs', 'Backgrounds']):
		user = User.find(User.ID == str(interaction.user.id)).first() if (str(interaction.user.id) in fetch_users()) else User(ID=str(interaction.user.id)).save()

		embed = Embed(title=f"{category} shop", description=f"Coins: {user.coins} :coin:\n\n", color=Color.default)

		for key, value in all_items[category.lower()].items():
			if (value['price'] <= 0): continue

			name = f"**{key.replace('_', ' ').capitalize()}**"
			if (value['price'] > user.coins): name = f"~~{key.replace('_', ' ').capitalize()}~~"

			embed.description += f"{value['icon']} - {name} `({value['price']}`:coin:`)`\n"

		if (user.coins <= 999): await interaction.response.send_message(embed=embed, ephemeral=True); return

		view = Shop_view(user, category.lower())
		msg = await interaction.response.send_message(embed=embed, view=view)
		await view.wait()
		await msg.delete()


def setup(bot):
	bot.add_cog(Shop_slash(bot))
