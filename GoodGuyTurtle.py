from util import *
import turtle

class GoodGuyTurtle(BaseTurtle):
	length = 0
	color = "green4"

	def __init__(self,startx,starty,length):
		GoodGuyTurtle.length = length
		self.good_guy = turtle.Turtle()
		self.good_guy.hideturtle()
		self.good_guy.speed("fastest")
		self.good_guy.tracer(1,3)
		#self.move((starty, startx))

	def drawTurtle(self):
		self.good_guy.clear()
		self.good_guy.pendown()
		
		self.good_guy.begin_fill()
		self.good_guy.pen(fillcolor=GoodGuyTurtle.color, pencolor=GoodGuyTurtle.color,
			pensize=15)
		self.good_guy.circle(5)
		self.good_guy.end_fill()


	def getPos(self):
		return convToGridPos(self.good_guy.pos())

	def move(self, coord):
		self.good_guy.penup()
		pos = convToGUIPos(coord)
		self.good_guy.goto(pos[0] + GoodGuyTurtle.length/2, pos[1])

	def resetTracer(self):
		self.good_guy.tracer(1,15) #1,5
		turtle.update()

	def reset(self):
		self.good_guy.clear()
		
		
	

