from TurtleGUI import *
from util import *
import random

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

	def newGame(self, nogui):
		if nogui:
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