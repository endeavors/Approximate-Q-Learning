from util import *
import turtle

class Monster(BaseTurtle):

	def __init__(self,starty,startx):
		self.monster = turtle.Turtle()
		self.monster.speed("fastest")
		self.monster.hideturtle()
		self.monster.tracer(1,2)
		self.move((starty, startx))
		
	def drawTurtle(self):
		self.monster.clear()
		self.monster.pendown()
		self.monster.fillcolor("red")
		self.monster.pencolor("red")
		self.monster.begin_fill()
		self.monster.circle(tri_length, steps=5)
		self.monster.end_fill()

	def getPos(self):
		return convToGridPos(self.monster.pos())

	def move(self, coord):
		self.monster.penup()
		pos = convToGUIPos(coord)
		self.monster.goto(pos[0] + ((tri_length)/2), pos[1] - ((tri_length)/2))

	def resetTracer(self):
		self.monster.tracer(1,15) #1,15 #0,0
		turtle.update()

	def reset(self):
		self.monster.clear()