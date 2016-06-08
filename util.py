from abc import ABCMeta, abstractmethod
import math, heapq

screen_width = 800
screen_height = 800
dotsize = 5
obj_size = dotsize * 2.5
sq_length = 2*obj_size * math.sin(math.pi/4)
tri_length = 1.5*obj_size * math.sin(math.pi/3)
origin = (-300, 300)
starty = int(math.ceil(origin[0] + (sq_length/2)))
startx = int(math.ceil(origin[0] + (sq_length/2)))
endy = int(math.ceil(origin[1] + (sq_length/2)))
endx = int(math.ceil(origin[1] + (sq_length/2))) 
gridsize = 10 #20
step = abs(origin[0] - origin[1])/gridsize #30
wall_length = 3
wall1_y = starty + (2 *step)
wall2_y = endy - (2*step)

lower_pris_x = gridsize - wall_length #16
upper_pris_x = gridsize - 1 #20
lower_pris_y = 0
upper_pris_y = 1



class BaseTurtle:
	__metaclass__ = ABCMeta

	@abstractmethod
	def drawTurtle(self):
		pass

	@abstractmethod
	def getPos(self):
		pass

	@abstractmethod
	def move(self,coord):
		pass

def convToGUIPos(listpos):
	x = listpos[1]
	y = listpos[0]
	return (int(origin[0] + (x * step)), int(origin[1] + (y * -step)))

def convToGridPos(listpos):
	x = listpos[0]
	y = listpos[1]
	return (int((origin[1]-y)/step), int((origin[0]-x)/(-step)))

def convYToGridPos(y):
	return int((origin[1]-y)/step)

def manhattan_dist(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])