from libs.pyeuclid import *
from pointset import PointSet

class ArenaMap(dict):
	class Marker(object):
		def __init__(center, zone):
			self.center = center
			self.zone = zone

			if zone == 0:
				side = Vector2(marker_width/2, 0) #right
			elif zone == 1:
				side = Vector2(0, marker_width/2) #up
			elif zone == 2:
				side = Vector2(-marker_width/2, 0) #left
			elif zone == 3:
				side = Vector2(0, -marker_width/2) #down

			self.left, self.right = center + side, center - side

	def __init__(self, arenaMarkers):
		self.update(arenaMarkers)

	def nearestMarkerTo(self, point):
		"""Find the marker with the minimum distance to the given point, and return its id"""
		return min(self, key = lambda i: abs(point - self[i].center))

	def positionsFromCodes(self, codes):
		positions = []
		for code in codes:
			pos = self[code]
			positions += [pos.right, pos.left]
		return PointSet(positions)

	def estimatePositionFrom(visionResult):
		"""Calculate the robot position given what it can see"""
		#commonMarkerIds = set(visionResult.keys()) & set(self.keys())
		apparent = visionResult.arenaMarkerEdges()
		actual = self.positionsFromCodes(visionResult)

		#Translation is the amount the origin is transformed
		return actual.bestTransformTo(apparent) * Point2(0, 0)