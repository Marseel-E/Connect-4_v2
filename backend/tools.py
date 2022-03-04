class Color:
	def __init__(self):
		self.green = int("77DD77", 16)
		self.blurple = int("5261f8", 16)
		self.red = int("ff6961", 16)
		self.clear = int("2f3136", 16)
		self.default = self.clear
		self.yellow = int("FDFD96", 16)
		self.white = int("f0f0f0", 16)
		self.black = int("000000", 16)
		self.blue = int("AEC6CF", 16)
Color = Color()


support_server_link = "https://discord.gg/DFDUpXJNdc"
support_server = f"[Support Server]({support_server_link})"
default_bot = "[Bot](https://top.gg/bot/795099690609279006)"


def check_permission(ctx, permission):
	return not (permission in [perm[0] for perm in list(ctx.author.guild_permissions) if perm[1]])
