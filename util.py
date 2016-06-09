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
gridsize = 15
step = abs(origin[0] - origin[1])/gridsize #30
wall_length = 4
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

class PriorityQueue():
	def __init__(self):
		self._queue = []
		self._index = 0

	def push(self,info):
		heapq.heappush(self._queue, (info[0],self._index,info))
		self._index += 1

	def pop(self):
		return heapq.heappop(self._queue)

	def empty(self):
		return not len(self._queue)

class AStar():
	def __init__(self,walls,actions):
		self.cost = 1
		self.walls = walls
		self.actions = actions

	def astar(self,start,goal):
		self.goal = goal
		self.start = start
		queue = PriorityQueue()
		path_list = []
		path_list.append(self.start)
		queue.push((self.cost + manhattan_dist(self.start,self.goal), self.start, path_list))
		
		while not queue.empty():
			curr_pos_tup = queue.pop()
			curr_fx, curr_state, curr_path = curr_pos_tup[2]
		
			if self.isGoal(curr_state):
				return len(curr_path)
			
			for child in self.getChildren(curr_state):
				cost = curr_fx - manhattan_dist(curr_state,self.goal)
				new_fx = manhattan_dist(child,self.goal) + (self.cost + cost)
				queue.push((new_fx, child, curr_path + [child]))
		

	def getChildren(self,curr_state):
		children = []
		curr_row, curr_col = curr_state
		map_states = map(lambda l: (curr_row+l[0],curr_col+l[1]),self.actions)

		for state in map_states:
			row, col = state
			if row >= 0 and row <= gridsize and col >= 0 and \
				col <= gridsize and (row,col) not in self.walls:
					children.append(state)

		return children
			
	def isGoal(self,state):
		return state == self.goal

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
