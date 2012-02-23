from libs.pyeuclid import *
from systemetric.bearing import Bearing
from pointset import PointSet

class ArenaMap(dict):
	class Marker(object):
		WIDTH = 0.25 * 10/12
		def __init__(self, center, zone):
			self.center = center
			self.zone = zone

			if zone == 0:
				side = Vector2(self.WIDTH/2, 0) #right
			elif zone == 1:
				side = Vector2(0, self.WIDTH/2) #up
			elif zone == 2:
				side = Vector2(-self.WIDTH/2, 0) #left
			elif zone == 3:
				side = Vector2(0, -self.WIDTH/2) #down

			self.left, self.right = center + side, center - side

	def __init__(self, size, arenaMarkers):
		self.size = size
		self.update(arenaMarkers)

	def nearestMarkerTo(self, point):
		"""Find the marker with the minimum distance to the given point, and return its id"""
		return min(self, key = lambda i: abs(point - self[i].center))

	def positionsFromCodes(self, visionResult):
		codes = [marker.id for marker in visionResult.arena]
		positions = []
		for code in codes:
			pos = self[code]
			positions += [pos.right, pos.left]

		return PointSet(positions), codes

	def getLocationInfoFrom(self, visionResult):
		if visionResult.arena:
			apparent = visionResult.arenaMarkerEnds()
			actual, codes = self.positionsFromCodes(visionResult)
			theta, transform, error = apparent.bestTransformTo(actual)

			info = lambda: magic #extendable_object

			info.heading = Bearing(radians=theta)
			info.transform = transform
			info.location = transform * Point2(0, 0)
			info.accuracy = error

			return info

	def estimateTransformFrom(self, visionResult):
		return getLocationInfoFrom(self, visionResult).transform