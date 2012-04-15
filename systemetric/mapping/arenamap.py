# This file is part of systemetric-student-robotics.

# systemetric-student-robotics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# systemetric-student-robotics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with systemetric-student-robotics.  If not, see <http://www.gnu.org/licenses/>.

from libs.pyeuclid import *
from systemetric.bearing import Bearing
from pointset import PointSet
import time
from systemetric.timer import Timer

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
		t = Timer()
		times = {}

		if visionResult.arena:
			with t.event("arenaMarkerEnds"):
				apparent = visionResult.arenaMarkerEnds()
			with t.event("positionsFromCodes"):
				actual, codes = self.positionsFromCodes(visionResult)
			with t.event("bestTransformTo"):
				theta, transform, error = apparent.bestTransformTo(actual)

			info = lambda: magic #extendable_object

			info.heading = Bearing(radians=theta)
			info.transform = transform
			info.location = transform * Point2(0, 0)
			info.accuracy = error

			print times
			return info

	def estimateTransformFrom(self, visionResult):
		return getLocationInfoFrom(self, visionResult).transform