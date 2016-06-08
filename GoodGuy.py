from TurtleGUI import *
from util import *
from collections import Counter
import time, math, random, sys
import numpy as np

class GameConfig():
	actions = {"N":(-1,0), "S": (1,0), "E": (0,1), "W": (0,-1)}
	GUY, MONSTER, PRISONER, WALL = range(1000, 1004)
	PRISONER_RW = 100
	MONSTER_RW = -100
	REST_RW = -10
	PROB_OF_ATTACK = 0.5
	MONS_NUM = 1
	PRIS_NUM = 4

	def __init__(self, turtle_gui):
		self.tur_gui = turtle_gui
		self.walls = [(convYToGridPos(wall1_y)+1,x) for x in range(wall_length+1)] + \
			[(convYToGridPos(wall2_y)+1,x) for x in range(gridsize-wall_length,gridsize+1)]
		#only get info from the GUI the first time, that's why we are in init
		self.drawAllTurtles()
		self.updateObjPoses()

	def updateObjPoses(self):
		self.prisoners_pos = map(lambda x: x.getPos(), self.tur_gui.prisoner_list)
		self.monsters_pos = map(lambda x: x.getPos(), self.tur_gui.monster_list)
		self.guy_pos = self.tur_gui.good_guy.getPos()

	def newGame(self):
		if QLearning.NOGUI:
			for x in range(len(self.tur_gui.monster_list)):
				mon_pos = GameConfig.genMonsNewPos()
				self.monsters_pos[x] = convToGridPos(mon_pos)

			for p_idx, pos in enumerate(GameConfig.genPrisPosList(len(self.prisoners_pos))):
				self.prisoners_pos[p_idx] = pos
				
		else:
			self.tur_gui.resetAllTurtles()
			self.drawAllTurtles()
			self.updateObjPoses()

	@staticmethod
	def genMonsNewPos():
		y = random.randint(TurtleGUI.lower_mons_y,TurtleGUI.upper_mons_y)
		x = random.randint(TurtleGUI.lower_mons_x,TurtleGUI.upper_mons_x)
		return (y,x)

	@staticmethod
	def genPrisNewPos():
		x = random.randint(lower_pris_x,upper_pris_x)
 		y = random.randint(lower_pris_y, upper_pris_y)
 		return (y,x)

 	@staticmethod
 	def genPrisPosList(pris_num):
 		pris_pos_list = []
		for x in range(pris_num):
			pos = GameConfig.genPrisNewPos()
			while pos in pris_pos_list:
				pos = GameConfig.genPrisNewPos()
			pris_pos_list.append(pos)
		return pris_pos_list

	def drawAllTurtles(self):
		self.tur_gui.addMonsters(GameConfig.MONS_NUM, [self.genMonsNewPos() \
			for x in range(GameConfig.MONS_NUM)])
		self.tur_gui.addPrisoners(GameConfig.PRIS_NUM, \
			self.genPrisPosList(GameConfig.PRIS_NUM))
		self.tur_gui.addGoodGuy()

	def getReward(self, state):
		if self.isMonsterPos(state):
			return GameConfig.MONSTER_RW
		elif self.getRewardPos == state:
			return GameConfig.PRISONER_RW
		else:
			return GameConfig.REST_RW

	def getRewardPos(self):
		if not self.isGameFinished():
			self.prisoners_pos.sort(key=lambda x: x[1])
			return self.prisoners_pos[0]
		return None

	def isGameFinished(self):
		for y,x in self.prisoners_pos:
			if y <= convYToGridPos(wall1_y)+1 and x >= wall_length:
				return False
		return True

	def isWallPos(self, state):
		return state in self.walls

	def isMonsterPos(self,state):
		return state in self.monsters_pos

	def isGuyPos(self,state):
		return state in self.guy_pos

	def isGoalState(self,state):
		rw_pos = self.getRewardPos()
		if rw_pos:
			return rw_pos == state
		return None

class QLearning():
	LEARNING_RATE = 0.5
	DISCOUNT_FACTOR = 0.6 
	EPISODES = 500
	TEMPERATURE = 30.0
	GAMES_TO_PLAY = 10
	NOGUI = False

	def __init__(self, turtle_gui, nogui=False):
		QLearning.NOGUI = nogui
		self.turtle_gui = turtle_gui
		self.gameConfig = GameConfig(turtle_gui)
		self.weight_vector = Counter()
		self.qLearn()

	def qLearn(self):
		for episode in range(QLearning.EPISODES + QLearning.GAMES_TO_PLAY):
			if episode >= QLearning.EPISODES:
				QLearning.NOGUI = False
				print "\nGame Playing", (episode + 1) - QLearning.EPISODES,
			else:
				print "\rTraining %d" % (episode + 1),
				sys.stdout.flush()

			curr_state = self.getStartStatePos() #start state
			

			while not self.gameConfig.isMonsterPos(curr_state) and \
				not self.gameConfig.isGoalState(curr_state):

					new_guy_pos_tup = self.getAction(curr_state,episode)
					mons_pos_acts = map(lambda pos: self.getMonsterLegalActions(pos), 
						self.gameConfig.monsters_pos)
					
					self.dispatchMovements(new_guy_pos_tup[0], mons_pos_acts,episode)

					immediate_reward = self.gameConfig.getReward(curr_state)
					curr_QVal = self.getQValue(curr_state,new_guy_pos_tup[1])
					max_qprime = self.getQPrimeVal()

					difference = (immediate_reward + QLearning.DISCOUNT_FACTOR * \
						max_qprime) - curr_QVal

					f_vector = self.getFeatures(curr_state, new_guy_pos_tup[1])
					for feature in f_vector:
						old_weight = self.weight_vector[feature]
						self.weight_vector[feature] = old_weight + QLearning.LEARNING_RATE \
							* difference * f_vector[feature]
					curr_state = self.gameConfig.guy_pos
			

			#new game
			self.gameConfig.newGame()


	def getQPrimeVal(self):
		max_list = []
		new_state = self.gameConfig.guy_pos
		legal_acts_dict = self.getLegalActions(new_state)
		for act in legal_acts_dict:
			max_list.append(self.getQValue(new_state,act))
		return max(max_list)

	def getAction(self,state, episode):
		act_prob_dict = self.getActionsProbs(state,episode)
		sorted_dict = sorted(act_prob_dict.items(), key=lambda x: x[1])
		weights = [val[1] for val in sorted_dict]
		acts = [val[0] for val in sorted_dict]
		sample = np.random.choice(acts,p=weights,size=1)[0]
		return (self.getNextState(state,sample), sample)
		

	def getNextState(self,state,action_str):
		base_move = self.gameConfig.actions[action_str]
		return (state[0]+base_move[0], state[1]+base_move[1])

	def getStartStatePos(self,isRandom=True):
		if isRandom:
			y = random.randint(0,gridsize-1)
			x = random.randint(0,gridsize-1)
			while self.gameConfig.isWallPos((y,x)) or self.gameConfig.isMonsterPos((y,x)) or\
				self.gameConfig.isGuyPos((y,x)):
				y = random.randint(0,gridsize-1)
				x = random.randint(0,gridsize-1)
			return (y,x)
		else:
			return (gridsize-2,wall_length)

	def getLegalActions(self,state):
		actions = {}
		for act_str, val in GameConfig.actions.items():
			zipy, zipx = zip(state,val)
			y = sum(zipy)
			x = sum(zipx)
			if y >= 0 and y < gridsize and x >= 0 and x < gridsize and \
				not self.gameConfig.isWallPos((y,x)):
				actions[act_str] = (y,x)
		
		return actions

	def getMonsterLegalActions(self,state):
		actions = {}
		for act_str, val in GameConfig.actions.items():
			zipy, zipx = zip(state,val)
			y = sum(zipy)
			x = sum(zipx)
			if y >= 0 and y < gridsize and x >= 0 and x < gridsize and \
				not self.gameConfig.isWallPos((y,x)) and y > TurtleGUI.lower_mons_y and \
				y < TurtleGUI.upper_mons_y and x > TurtleGUI.lower_mons_x and \
				x < TurtleGUI.upper_mons_x:
				actions[act_str] = (y,x)
		return actions

	def getFeatures(self,state,action):
		#next location guy good based on given action
		base_move = self.gameConfig.actions[action]
		next_pos = (state[0] + base_move[0], state[1] + base_move[1])

		dist_to_rw = manhattan_dist(next_pos,self.gameConfig.getRewardPos())
		dist_to_mon = min([manhattan_dist(next_pos,mon_pos) for mon_pos in \
			self.gameConfig.monsters_pos])
		features = Counter()	
		features["dist_to_rw"] = dist_to_rw/100.0
		features["ghosts_num"] = sum(next_pos in self.getMonsterLegalActions(mon_pos) \
			for mon_pos in self.gameConfig.monsters_pos)

		return features

	def getQValue(self,state, action):
		q_val = 0
		feature_vector = self.getFeatures(state,action)
		for feature in feature_vector:
			q_val += self.weight_vector[feature] * feature_vector[feature]
		return q_val

	def getActionsProbs(self,state,episode):
		#Boltzmann exploration optimization
		#Probability of (action | state)
		probs = {}
		tDiff = QLearning.TEMPERATURE/QLearning.EPISODES
		T = QLearning.TEMPERATURE - (tDiff * episode) + 1
		
		actions = self.getLegalActions(state)
		deno = sum([math.exp((self.getQValue(state, act))/T) for act in actions])
		for act in actions:
			prob = 0
			qVal = self.getQValue(state,act)
			numer = math.exp(qVal/T)
			if deno != 0:
				prob = numer/deno
			probs[act] = prob

		#normalize
		total = sum(probs.values())
		for key,val in probs.items():
			val /= total

		return probs

	def dispatchMovements(self,guy_new_pos, mons_acts,episode):
		#update guy position
		old_guy_pos = self.gameConfig.guy_pos
		self.gameConfig.guy_pos = guy_new_pos
		

		#update monsters position
		#mons_acts is [{},{}] of all legal actions
		for mon_idx, mon_act in enumerate(mons_acts):
			if mon_act:
				distToGuy = [(manhattan_dist(old_guy_pos,pos_tup),dir_str) for \
					dir_str,pos_tup in mon_act.items()]
				manhattan_dists = map(lambda x: x[0], distToGuy)
				minDist = min(manhattan_dists)
				bestActions = [distToGuy[idx][1] for idx, dist in enumerate(manhattan_dists) \
					if dist == minDist]

				distribution = Counter()
				for act in bestActions:
					distribution[act] = self.gameConfig.PROB_OF_ATTACK/ len(bestActions)
				for act in mon_act:
					distribution[act] += (1 - self.gameConfig.PROB_OF_ATTACK) / \
						len(mon_act)
				#normalizing
				total_sum = float(sum(distribution.values()))
				if total_sum != 0:
					for k in distribution.keys():
						distribution[k] /= total_sum

				dist_keys = distribution.keys()
				dist_keys.sort()
				dist_values = [distribution[key] for key in dist_keys]
				sample = np.random.choice(dist_keys,p=dist_values,size=1)[0]

				#two monsters shouldn't be in the same position
				prev_mon_pos = self.gameConfig.monsters_pos[mon_idx - 1]
				if idx != 0 and mon_act[sample] == prev_mon_pos:
					while mon_act[sample] == prev_mon_pos:
						i = random.randint(0,len(mon_act)-1)
						sample = dist_keys[i]
				self.gameConfig.monsters_pos[mon_idx] =  mon_act[sample]

		if not QLearning.NOGUI or episode >= QLearning.EPISODES:
			self.turtle_gui.good_guy.move(guy_new_pos)
			self.turtle_gui.good_guy.drawTurtle()

			for idx, mon in enumerate(self.turtle_gui.monster_list):
				mon.move(self.gameConfig.monsters_pos[idx])
				mon.drawTurtle()
		

def main():
	turtle.title ('The Good Guy')
  	turtle.setup (screen_width, screen_height, None, None)
  	turtle_gui = TurtleGUI()

	QLearning(turtle_gui,True)
	
	turtle.done()
	

if __name__ == '__main__':
	main()