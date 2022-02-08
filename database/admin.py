import json

from pprint import pprint

from main import *


def install_old_database():
	print("old size:", redis.dbsize(), "\n")

	with open("discord-bot-101df-export.json", 'r') as f:
		data = json.loads(f.read())
		pprint(data)

		check = input("\nIs that correct?\n")
		if not (check): exit()

		check = input("\nFlush database?\n")
		if not (check): exit()
		print(redis.flushall())

		for key, value in data['connect-4'].items():
			if key == "developers": continue
			if key == "games": continue

			if key == "guilds":
				check = input("\nAdd guilds?\n")
				if not (check): exit()

				for key, value in value.items():
					Guild(ID=str(key), prefix=value['prefix']).save()
					print("Added guild")

			if key == "users":
				check = input("\nAdd users?\n")
				if not (check): exit()

				for key, value in value.items():
					try: (value['inventory'])
					except: inventory = {"discs": ["blue_circle","orange_circle"],
										"backgrounds": ["black_circle"],
										"embed_colors": ["5261f8"]}
					else: inventory = {'discs': list(value['inventory']['discs'].keys()), 'backgrounds': list(value['inventory']['backgrounds'].keys()), 'embed_colors': list(value['inventory']['embedColors'].values())}

					User(ID=str(key), background=value['background'], coins=value['cash'], stats={'wins': value['wins'], 'loses': value['loses'], 'draws': value['draws']}, exp=value['exp'], level=value['level'], primary_disc=value['primaryDisc'], secondary_disc=value['secondaryDisc'], embed_color=value['embedColor'], inventory=inventory).save()
					print("added user")

	print("done!")
	print("\nnew size:", redis.dbsize())


if __name__ == '__main__':
	while True:
		print(eval(input('>>> ')))