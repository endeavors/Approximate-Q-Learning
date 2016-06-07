from util import *

class Publisher:
	def __init__(self):
		self.subs = set()

	def register(self, sub):
		self.subs.add(sub)

	def unregister(self, sub):
		self.subs.discard(sub)

	def dispatch(self, pos, gameConfig, mons_acts,turtle_gui):
		#the good guy will be the only one calling this method
		for sub in self.subs:
			sub.update(pos, gameConfig, mons_acts)

class Subscriber:
	def __init__(self):
		pass

	def update(self,pos, gameConfig, mons_acts,turtle_gui):
		pass