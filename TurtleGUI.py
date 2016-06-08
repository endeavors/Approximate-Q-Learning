from util import *
import turtle, random, Monster, Prisoner, GoodGuyTurtle

class TurtleGUI():
	lower_mons_y = convYToGridPos(wall2_y) + 2
	upper_mons_y = convYToGridPos(wall1_y) 
	lower_mons_x = 0
	upper_mons_x = gridsize - 1

	def __init__(self):
		self.prisoner_list = []
  		self.monster_list = []
  		self.good_guy = None
  		self.__drawGrid()

	def __drawGrid(self):
		gridTurtle = turtle.Turtle()
		gridTurtle.hideturtle()
		gridTurtle.tracer(40,0)
  		for y in range (starty, endy + 1, step):
			gridTurtle.penup()
			gridTurtle.goto (startx, y)
			gridTurtle.pendown()
			gridTurtle.dot(dotsize, "gray")
			for x in range(startx + step, endx + 1, 
				step):
				gridTurtle.penup()
				gridTurtle.goto(x,y)
				gridTurtle.pendown()
				gridTurtle.dot(dotsize, "gray")

		gridTurtle.penup()
		gridTurtle.pen(pensize=dotsize, pencolor="green")
		gridTurtle.goto(startx, wall1_y)
		gridTurtle.pendown()
		gridTurtle.forward(wall_length*step)

		gridTurtle.penup()
		gridTurtle.pen(pencolor="black")
		gridTurtle.goto(endx - (wall_length*step), wall2_y)
		gridTurtle.pendown()
		gridTurtle.forward(wall_length*step)
		gridTurtle.penup()

		
	def addMonsters(self,monster_num,pos):
		for num in range(monster_num):
			monster = Monster.Monster(pos[num][0],pos[num][1])
			monster.drawTurtle()
			self.monster_list.append(monster)
 
 	def addPrisoners(self,prisoner_num, pos):
 		for num in range(prisoner_num):
 			prisoner = Prisoner.Prisoner(pos[num][0],pos[num][1])
 			prisoner.drawTurtle()
 			self.prisoner_list.append(prisoner)
 			
 	def addGoodGuy(self):
 		self.good_guy = GoodGuyTurtle.GoodGuyTurtle()
 		#self.good_guy.drawTurtle() #commented out
 		self.good_guy.resetTracer()

 	def resetAllTurtles(self):
 		self.good_guy.reset()
 		for prisoner in self.prisoner_list:
 			prisoner.reset()

 		for monster in self.monster_list:
 			monster.reset()
 		del self.monster_list[:]
 		del self.prisoner_list[:]

	
