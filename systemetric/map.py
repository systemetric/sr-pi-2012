from libs.pyeuclid import *
from copy import copy
class Map(object):
	"""Stores a map of the arena"""
	def __init__(self, arena):
		self.arena = arena
		self.tokens = {}
		self.buckets = {}
		self.robot = None

	def fakeUpdateEntities(self, transform, tokens):
		"""Used for vision-less testing"""
		for id, position in tokens.iteritems():
			self.tokens[id] = position

		self.robot = transform

	def updateEntityLocations(self, pvr, transform):
		"""Update the map with the new set of vision information"""

		#TODO: Maybe keep a timestamp on tokens, and "forget" them after a while?
		self.robot = self.arena.getLocationInfoFrom(pvr)
		if self.robot:
			for token in pvr.tokens:
				self.tokens[token.id] = copy(token)
				self.tokens[token.id].transform(transform.inverse())