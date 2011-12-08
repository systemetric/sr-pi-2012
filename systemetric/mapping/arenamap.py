from libs.pyeuclid import *

class ArenaMap(object)
	def __init__(self):
		if not self.zones:
			raise NotImplementedError("You must derive from ArenaMap - it is abstract")

		#Magic line of code - joins all the wall dictionaries into one dictionary
		self.all = dict(sum((zone.items() for zone in self.zones), []))

	def nearestMarkerTo(point):
		"""Find the marker with the minimum distance to the given point, and return its id"""
		return min(self.all, key = lambda i: abs(point - self.all[i]))

	def estimatePositionFrom(markers):
		"Calculate the robot position given the"
		pass