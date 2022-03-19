from __future__ import annotations

from redis_om import (HashModel, JsonModel, Field, Migrator)
from typing import Optional, Union
from dotenv import load_dotenv
from pprint import pprint
from redis import Redis
from os import environ

load_dotenv('../.env')

redis = Redis(host=environ.get("DB_HOST"), port=environ.get("DB_PORT"), db=environ.get("DB_N"), password=environ.get("DB_PASSWORD"))

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


def fetch_users() -> list: return [user.ID for user in User.find(User.ID != '0').all()]
def fetch_guilds() -> list: return [guild.ID for guild in Guild.find(Guild.ID != '0').all()]
def fetch_games() -> list: return [game.ID for game in Game.find(Game.ID != '0').all()]

def get_user(ID: str) -> User: return User.find(User.ID == str(ID)).first() if (str(ID) in fetch_users()) else User(ID=str(ID)).save()


if __name__ == '__main__':
	while True:
		print(eval(input(">>> ")))