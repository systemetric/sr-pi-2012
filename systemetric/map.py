from libs.pyeuclid import *
from copy import copy
from time import time
class Map(object):
	"""Stores a map of the arena"""
	class Entity(object):
		def __init__(self, type, id, position = None, timestamp = 0):
			self.type = type
			self.position = position
			self.timestamp = timestamp
			self.id = id

		@property
		def reliability(self):
			HALF_LIFE = 10 #Time in seconds for an item to become half as likely
			dt = time() - self.timestamp

			return 2.0**(-dt/HALF_LIFE)

		def invalidate(self):
			self.timestamp = 0

		def desirability(robotpos):
			distance = abs(robotpos - self.position)

			return self.reliability / distance
		@property
		def exists(self):
			return self.timestamp != 0

		def __repr__(self):
			return '<Map.Entity %s #%d at %s>' % (self.type, self.id, self.position)

	def __init__(self, arena):
		self.arena = arena
		self.tokens    = [Map.Entity('Token', i)  for i in range(20)]
		self.buckets   = [Map.Entity('Bucket', i) for i in range(4)]
		self.opponents = [Map.Entity('Robot', i)  for i in range(4)]
		self.robot = None

	def fakeUpdateEntities(self, transform, tokens):
		"""Used for vision-less testing"""
		t = time()
		for id, position in tokens.iteritems():
			self.tokens[id].timestamp = t
			self.tokens[id].position = position

		self.robot = transform

	def invalidateRobotPosition(self):
		self.robot = None

	def updateEntities(self, vision):
		"""Update the map with the new set of vision information"""

		#TODO: Maybe keep a timestamp on tokens, and "forget" them after a while?
		locInfo = self.arena.getLocationInfoFrom(vision)
		if locInfo:
			self.robot = locInfo
			
			for token in vision.tokens:
				if token.captured:
					print "token %s captured" % token.id
					self.tokens[token.id].invalidate()
				else:
					self.tokens[token.id].position  = locInfo.transform * token.center
					self.tokens[token.id].timestamp = vision.timestamp