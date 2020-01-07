import time
import numpy as np
import math
from aworld_client_core import Core, config

actions = [
		'up',
		'left',
		'right',
		'down',
		'spacebar',
		'i'
		]


def make_param(action_name):
	optional = {}
	if action_name == "up" or action_name == 0:
		optional["speed"] = 0.025
	elif action_name == "left" or action_name == 2:
		optional["angle"] = 0.01
	elif action_name == "right" or action_name == 3:
		optional["angle"] = 0.01
	elif action_name == "down" or action_name == 1:
		optional["speed"] = 0.005
	elif action_name == "i" or action_name == 4:
		optional["item_index"] = 0
	return optional

class Env():
	def __init__(this):
		pass

	def sample(this):
		cid = this.core.data.character_id
		probs = np.random.rand(len(actions))
		if cid and cid in this.core.data.characters:
			pc = this.core.data.characters[cid]
			terrain = this.core.data.terrain
			x = pc['x']
			y = pc['y']
			angle = pc['angle']
			fx = int(np.floor(x + np.cos(angle) * 0.025))
			fy = int(np.floor(y + np.sin(angle) * 0.025))
			if terrain.map[fy][fx] == 0:
				probs[actions.index('up')] = np.inf
			else:
				probs[actions.index('right')] = np.inf
		action = actions[probs.argmax()]
		return action

	def reset(this):
		this.core = Core()
		this.core.spawn_thread(secure=False)
		this.core.send_key('login')

		this.reward = 0
		observation = []
		
		while True:
			observation = [[0 for _ in range(10)] for _ in range(10)]

			cid = this.core.data.character_id

			action = this.sample()

			if cid and cid in this.core.data.characters:
				pc = this.core.data.characters[cid]
				terrain = np.ones((120,120))
				terrain2 = np.array(this.core.data.terrain.map)
				for i in range(0,50):
					for j in range(0,50):
						terrain[i + 10][j + 10] = terrain2[i][j]
				x = math.floor(pc['x']) + 10
				y = math.floor(pc['y']) + 10
				angle = pc['angle']
				fx = int(np.floor(x + np.cos(angle) * 0.025))
				fy = int(np.floor(y + np.sin(angle) * 0.025))

				print(this.core.data.terrain.map)
				print(terrain, x, y)
				print(terrain[x - 5:x + 5,y - 5:y + 5])

				observation = [terrain[x - 5:x + 5,y - 5:y + 5]]
				break

			this.step(action)
			print(action)
			time.sleep(0.05)

		return np.array(observation)


	def step(this, action):
		print("action=", action)
		action_name = ""
		if action == "up" or action == 0:
			action_name="up"
		elif action == "left" or action == 2:
			action_name="left"
		elif action == "right" or action == 3:
			action_name="right"
		elif action == "down" or action == 1:
			action_name="down"
		elif action == "i" or action == 4:
			action_name="i"
		else:
			action_name = "spacebar"
		
		this.core.send_key(action_name, True, make_param(action_name))
		time.sleep(0.01)
		this.core.send_key(action_name, False)
		
		observation, reward, done, info = [], 0, False, {}

		cid = this.core.data.character_id
		probs = np.random.rand(len(actions))
		if cid and cid in this.core.data.characters:
			pc = this.core.data.characters[cid]
			terrain = np.ones((120,120))
			terrain2 = np.array(this.core.data.terrain.map)
			for i in range(0,50):
					for j in range(0,50):
						terrain[i + 10][j + 10] = terrain2[i][j]
			x = math.floor(pc['x']) + 10
			y = math.floor(pc['y']) + 10
			angle = pc['angle']
			fx = int(np.floor(x + np.cos(angle) * 0.025))
			fy = int(np.floor(y + np.sin(angle) * 0.025))

			this.reward += 1

			observation = [terrain[x - 5:x + 5,y - 5:y + 5]]
			reward = this.reward
			done = False
			info = {}
			
			print(terrain[x - 5:x + 5,y - 5:y + 5])

		return np.array(observation), reward, done, info