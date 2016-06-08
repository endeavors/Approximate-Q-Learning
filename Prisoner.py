from util import *
import turtle, random

class Prisoner(BaseTurtle):

	def __init__(self,starty,startx):
		self.prisoner = turtle.Turtle()
		self.prisoner.speed("fastest")
		self.prisoner.tracer(1,1)
		self.prisoner.hideturtle()
		self.move((starty,startx))

	def drawTurtle(self):
		self.prisoner.clear()
		self.prisoner.begin_fill()
		color = self.getRandomColor()
		self.prisoner.fillcolor(color)
		self.prisoner.pencolor(color)
		self.prisoner.pendown()
		for i in range(4):
			self.prisoner.forward(sq_length)
			self.prisoner.left(360/4)
		self.prisoner.end_fill()

	def getPos(self):
		return convToGridPos(self.prisoner.pos())

	def getRandomColor(self):
		color_list = ["violet", "orange", "cyan", "black", "brown", "royal blue"]
		self.curr_color = color_list[random.randint(0,len(color_list)-1)]
		return self.curr_color

	def getCurrColor(self):
		return self.curr_color

	def move(self, coord):
		self.prisoner.penup()
		pos = convToGUIPos(coord)
		self.prisoner.goto(pos[0], pos[1])

	def reset(self):
		self.prisoner.clear()
