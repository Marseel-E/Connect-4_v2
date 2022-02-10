from discord import Embed, ui, Interaction, SelectOption
from typing import Literal
import slash_util as slash

from backend.items import items as all_items
from backend.tools import *

from database.main import *


class Buy_dropdown(ui.Select):
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


class Shop_view(ui.View):
	def __init__(self, user, category):
		super().__init__()
		self.user = user

		self.add_item(Buy_dropdown(self.user, category))

	async def interaction_check(self, interaction : Interaction):
		return (str(interaction.user.id) == self.user.ID)


class Shop_slash(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	@slash.slash_command()
	async def shop(self, ctx : slash.Context, category : Literal['Discs', 'Backgrounds']):
		user = User.find(User.ID == str(ctx.author.id)).first() if (str(ctx.author.id) in fetch_users()) else User(ID=str(ctx.author.id)).save()

		embed = Embed(title=f"{category} shop", color=Color.default)	

		description = f"Coins: {user.coins} :coin:\n\n"
		for key, value in all_items[category.lower()].items():
			if (value['price'] <= 0): continue

			name = f"**{key.replace('_', ' ').capitalize()}**"
			if (value['price'] > user.coins): name = f"~~{key.replace('_', ' ').capitalize()}~~"

			description += f"{value['icon']} - {name} `({value['price']}`:coin:`)`\n"
		embed.description = description

		if (user.coins <= 999): await ctx.send(embed=embed, ephemeral=True); return

		view = Shop_view(user, category.lower())
		msg = await ctx.send(embed=embed, view=view)
		await view.wait()
		await msg.delete()


def setup(bot):
	bot.add_cog(Shop_slash(bot))