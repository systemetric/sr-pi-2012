from libs.pyeuclid import *

class ArenaMarker(object):
	def __init__(center, zone):
		self.center = center
		self.zone = zone

		if zone == 0:
			side = Vector2(marker_width/2, 0)
		elif zone == 1:
			side = Vector2(0, marker_width/2)
		elif zone == 2:
			side = Vector2(-marker_width/2, 0)
		elif zone == 3:
			side = Vector2(0, -marker_width/2)

		self.left, self.right = center + side, center - side

class ArenaMap(dict):
	def __init__(self, arenaMarkers):
		self.update(arenaMarkers)

	def nearestMarkerTo(point):
		"""Find the marker with the minimum distance to the given point, and return its id"""
		return min(self, key = lambda i: abs(point - self[i].center))

	def positionsFromCodes(codes):
		positions = []
		for code in codes:
			pos = self[code]
			positions += [pos.right, pos.left]
		return positions

	def estimatePositionFrom(visionResult):
		"Calculate the robot position given the"
		apparent = visionResult.arenaMarkerEdges()
		actual = positionsFromCodes(visionResult)

		return actual.bestTransformTo(apparent) * Point2()