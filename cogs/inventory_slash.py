from discord import Embed, ui, ButtonStyle, Interaction, SelectOption
import slash_util as slash
from typing import Literal

from backend.tools import *
from backend.items import items as all_items

from database.main import *


class Disc_placements(ui.Select):
	def __init__(self):
		options = [
			SelectOption(label="Primary", description="Set this disc as your primary disc."),
			SelectOption(label="Secondary", description="Set this disc as your secondary disc."),
		]

		super().__init__(placeholder="Primary or Secondary?", min_values=1, max_values=1, options=options)

	async def callback(self, select : ui.Select, interaction : Interaction):
		self.view.primary_disc = True if select.values[0].lower() == "primary" else False
		self.view.stop()


class Select_item(ui.Select):
	def __init__(self, items):
		self.items = items
		options = [SelectOption(label=item.replace('_', ' ').capitalize(), description="") for item in self.items if (item not in [self.view.user.primary_disc, self.view.user.secondary_disc, self.view.user.background, self.view.user.embed_color])]

		super().__init__(placeholder="Select", min_values=1, max_values=1, options=options)

	async def callback(self, select : ui.Select, interaction : Interaction):
		self.view.value = select.values[0].lower().replace(' ', '_')
		self.view.stop()


class Use_button(ui.Button):
	def __init__(self):
		super().__init__(label="Use", style=ButtonStyle.blurple)

	async def callback(self, button : ui.Button, interaction : Interaction):
		print(self.view)
		print(self.view.value)
		self.view.value == "use"
		button.disabled = True
		self.view.stop()


class Inv_view(ui.View):
	def __init__(self, user):
		super().__init__()
		self.value = None
		self.primary_disc = True
		self.user = user

	async def interaction_check(self, interaction : Interaction):
		return str(interaction.user.id) == self.user.ID


class Inv_slash(slash.Cog):
	def __init__(self, bot):
		self.bot = bot


	@slash.slash_command(guild_id=843994109366501376)
	async def inventory(self, ctx : slash.Context, category : Literal['Discs', 'Backgrounds']):
		user = User.find(User.ID == str(ctx.author.id)).first() if str(ctx.author.id) in fetch_users() else User(ID=str(ctx.author.id)).save()
		category = category.lower().replace(' ', '_')

		items = ""
		for item in user.inventory[category]:
			items += f"{all_items[category][item]['icon']} - {item.replace('_', ' ').capitalize()}\n"

		embed = Embed(title="Inventory", description=items, color=Color.default)

		view = Inv_view(user)
		view.add_item(Use_button())

		msg = await ctx.send(embed=embed, view=view)
		await view.wait()

		if view.value == None: await msg.delete(); return
		await ctx.send(view.value, ephemeral=True)

		view.clear_items()
		view.add_item(Select_item(user.inventory[category]))

		await msg.edit(embed=embed, view=view)
		await view.wait()

		if view.value == None: await msg.edit(); return

		new_item = all_items[category][view.value]['icon']

		if (category == "discs"):
			view.clear_items()
			view.add_item(Disc_placements())

			await msg.edit(content="", embed=Embed.Empty, view=view, ephemeral=True)
			await view.wait()

			if (view.primary_disc):
				user.update(primary_disc=new_item)
				placement = "primary "
			
			else:
				user.update(secondary_disc=new_item)
				placement = "seconadry "

		if (category == "backgrounds"): user.update(background=new_item)

		view.clear_items()
		await msg.edit(content=f"{new_item} is your new `{placement}{category[:-1]}`", embed=Embed.Empty, view=view, ephemeral=True)


def setup(bot):
	bot.add_cog(Inv_slash(bot))