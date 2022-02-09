from redis import Redis

from redis_om import (HashModel, JsonModel, Field, Migrator)
from typing import Optional, Union
from pprint import pprint

redis = Redis(host='redis-11026.c241.us-east-1-4.ec2.cloud.redislabs.com', port=11026, db=0, password="xdaBgyVkr6gELOBNKtPvh8cxbX3NSc5Y")

OWNER = '470866478720090114'


class User(JsonModel):
	ID             : str = Field(index=True)
	coins          : Optional[int] = 1000
	exp            : Optional[int] = 0
	level          : Optional[int] = 1
	playing        : Optional[bool] = False
	embed_color    : Optional[str] = "5261f8"
	primary_disc   : Optional[str] = ":blue_circle:"
	background     : Optional[str] = ":black_circle:"
	secondary_disc : Optional[str] = ":orange_circle:"
	stats          : Optional[dict] = {'wins': 0, 'loses': 0, 'draws': 0}
	inventory      : Optional[dict] = {"discs": ["blue_circle","orange_circle"],
										"backgrounds": ["black_circle"],
										"embed_colors": ["5261f8"]}
	class Meta:
		database = redis

class Game(JsonModel):
	ID          : str = Field(index=True)
	players     : Optional[list] = []
	turn        : Optional[str] = None
	finished    : Optional[bool] = False
	board       : Optional[list] = [['0']*7]*6
	status      : Optional[str] = None
	message     : Optional[str] = None
	class Meta:
		database = redis

class Guild(HashModel):
	ID     : str = Field(index=True)
	prefix : Optional[str] = 'c-'
	class Meta:
		database = redis


Migrator().run()


def fetch_users():
	return [user.ID for user in User.find(User.ID != '0').all()]

def fetch_guilds():
	return [guild.ID for guild in Guild.find(Guild.ID != '0').all()]

def fetch_games():
	return [game.ID for game in Game.find(Game.ID != '0').all()]

if __name__ == '__main__':
	while True:
		print(eval(input(">>> ")))
