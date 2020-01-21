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
	acts = actions
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

				observation = np.zeros((700, 700, 3))
				break

			this.step(action)
			print(action)
			time.sleep(0.05)
		print(observation)
		return observation


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
			terrain = np.zeros((700,700,3))
			terrain2 = np.array(this.core.data.terrain.map)

			x = math.floor(pc['x'])
			y = math.floor(pc['y'])
			angle = pc['angle']
			fx = int(np.floor(x + np.cos(angle) * 0.025))
			fy = int(np.floor(y + np.sin(angle) * 0.025))

			for i in range(max(0, x - 3),min(x + 3, 100)):
				for j in range(max(0, y - 3),min(y + 3, 100)):
					for k in range(0, 10):
						for l in range(0, 10):
							if terrain2[i][j] == 1:
								terrain[i + k][j + l] = (0, 0, 255);
							elif terrain2[i][j] == 0:
								terrain[i + k][j + l] = (0, 255, 0);

			for character in this.core.data.characters.values():
				print("characters =", character)

				cx = math.floor(character['x'])
				cy = math.floor(character['y'])
			
				if x - 3 <= cx and cx <= x + 3 and y - 3 <= cy and cy <= y + 3:
					a = (x - cx) * 100 + 350
					b = (y - cy) * 100 + 350

					terrain[a][b] = (255,0,0)
					terrain[a - 1][b] = (230,0,0)
					terrain[a - 2][b] = (200,0,0)
					terrain[a][b - 1] = (230,0,0)
					terrain[a][b - 2] = (200,0,0)
					terrain[a + 1][b] = (230,0,0)
					terrain[a + 2][b] = (200,0,0)
					terrain[a][b + 1] = (230,0,0)
					terrain[a][b + 2] = (200,0,0)

			this.reward += 1

			observation = terrain
			reward = this.reward
			done = False
			info = {}
			
			print(terrain, terrain.shape)

		return observation, reward, done, info