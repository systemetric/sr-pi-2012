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
from systemetric.profiler import Profiler
import systemetric.logs as logs

class ArenaMap(dict):
	"""
	A class storing the arrangement of markers in a conceptual map of the arena

	:arg size: The size of the arena
	:type size: :class:`pyeuclid.Point2`
	:arg arenaMarkers: A :class:`dict` of integer - :class:`Marker` pairs

	"""
	class Marker(object):
		"""
		A class to store information about a marker in a conceptual map of the
		arena. Markers are represented as line segments between their left and
		right edges.

		.. attribute:: center
		               left
		               right
		   
		   :type: :class:`pyeuclid.Point2`
		   The left, right, and center of the marker, when projected down to 2d on a plane

		.. attribute:: zone
		   
		   the numeric id of the zone the marker belongs to, from 0 to 3. Used
		   to determine the orientation
		"""
		WIDTH = 0.25 * 10/12
		"""The size of the black area of the marker"""

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
		"""Finds corresponding marker definitions for the ones seen by the robot"""
		codes = [marker.id for marker in visionResult.arena]
		positions = []
		for code in codes:
			pos = self[code]
			positions += [pos.right, pos.left]

		return PointSet(positions), codes

	def getLocationInfoFrom(self, visionResult):
		"""
		Determine where the robot is, using a vision capture

		:returns: struct
		          
		          .. attribute:: heading

		             :type: :class:`Bearing`
		             The orientation of the robot

		          .. attribute:: transform

		             :type: :class:`Matrix3`
		             transformation matrix which maps percieved location to
		             actual location

		          .. attribute:: location

		             :type: :class:`Point2`
		             The location of the robot

		          .. attribute:: accuracy

		             :type: :class:`Point2`
		             An indication of the accuracy of the calculation - the
		             sum of the squares of the distances between actual and
		             apparent marker locations

		If no markers can bee seen, then ``None`` is returned. This function
		call is profiled to :data:`.logs.vision`.
		"""
		t = Profiler() >> logs.vision

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

			return info

	def estimateTransformFrom(self, visionResult):
		"""Shorthand for ``getLocationInfoFrom(visionResult).transform``"""
		locInfo = self.getLocationInfoFrom(visionResult)
		return locInfo.transform if locInfo else None