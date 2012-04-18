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
from systemetric.mapping import PointSet
from collections import defaultdict

import sr

class ProcessedVisionResult(object):
	"""
	2d representation of what can be seen

	.. attribute:: timestamp

		The time that the vision was captured

	.. attribute:: arena

		:type: list(:class:`~.ProcessedVisionResult.ArenaMarker`)
		The arenamarkers which can be seen

	.. attribute:: tokens

		:type: list(:class:`~.ProcessedVisionResult.Token`)
		The tokens which can be seen

	.. attribute:: buckets

		:type: list(:class:`~.ProcessedVisionResult.Bucket`)
		The buckets which can be seen

	.. attribute:: robots
	
		:type: list(:class:`~.ProcessedVisionResult.Robot`)
		The buckets which can be seen

	"""
	class ArenaMarker(object):
		"""
		A marker around the walls of the arena. The marker is projected down
		from a square to a line.

		.. attribute:: id

			the numeric id of the marker - from 0 to 27

		.. attribute:: left

			:type: :class:`pyeuclid.Point2`
			The leftmost edge of the marker, when viewed from the front

		.. attribute:: right

			:type: :class:`pyeuclid.Point2`
			The rightmost edge of the marker, when viewed from the front

		"""
		def __init__(self, visionResult, marker):
			self.id = marker.code

			#Convert points to 2D, and find midpoints
			v = [visionResult.planarLocationOf(v) for v in marker.vertices]

			#Midpoints of the sides
			mid1 = (v[0] + v[1]) / 2.0
			mid2 = (v[1] + v[2]) / 2.0
			mid3 = (v[2] + v[3]) / 2.0
			mid4 = (v[3] + v[0]) / 2.0

			#distance between opposite midpoints
			d1 = abs(mid1 - mid3)
			d2 = abs(mid2 - mid4)

			midpoints = (mid1, mid3) if d1 > d2 else (mid2, mid4)
			
			#Calculate sin(angle between edges[0], the origin, and edges[1])
			sinAngle = midpoints[0].left_perpendicular().dot(midpoints[1])

			theOrigin = Point2()

			if sinAngle > 0:
				#First point is to the left [CHECK!] of second point
				self.left = theOrigin + midpoints[0]
				self.right = theOrigin + midpoints[1]
			else:
				#First point is to the right [CHECK!] of second point
				self.left = theOrigin + midpoints[1]
				self.right = theOrigin + midpoints[0]

		def transform(self, matrix):
			self.left = matrix * self.left;
			self.right = matrix * self.right;

		def __repr__(self):
			return "<ArenaMarker #%d at %s, %s>" % (self.id, repr(self.left), repr(self.right))

	class Token(object):
		"""
		A cardboard cube. Groups all the markers of the same id into a single
		object, and calculates where the center of the cube should be, by
		pushing the normal vector of each surface back inside the cube.

		.. attribute:: id

			the numeric id of the marker - from 0 to 19

		.. attribute:: center

			:type: :class:`pyeuclid.Point3`

		.. attribute:: markers

			:type: list of :class:`Marker`
			The markers seen which correspond to this token

		.. attribute:: captured

			Guesses whether the cube is captured, by checking if it is more than
			0.5 meters off the ground

		"""
		SIZE = 0.1
		def __init__(self, visionResult, id, markers):
			self.id = id
			self.markers = markers
			center = sum(m.center - m.normal * self.SIZE / 2 for m in markers) / len(markers)
			self.captured = center.y > 0.5
			self.center = visionResult.planarLocationOf(center)

		def transform(self, matrix):
			self.center = matrix * self.center

		def __repr__(self):
			return "<Token #%d at %s>" % (self.id, repr(self.center))

	class Robot(object):
		SIZE = 0.5
		def __init__(self, visionResult, markers):
			self.markers = markers
			center = sum(m.center - m.normal * self.SIZE / 2 for m in markers) / len(markers)
			self.center = visionResult.planarLocationOf(center)

	class Bucket(object):
		"""
		The bucket with wheels. Used to store tokens.
		"""
		LENGTH = 0.372
		WIDTH  = 0.245
		def __init__(self, visionResult, id, markers):
			self.id = id

			#Find the center
			center = sum(
				m.center - m.normal * (
					self.LENGTH if m.type == sr.MARKER_BUCKET_END else self.WIDTH
				) / 2 for m in markers
			) / len(markers)
			self.center = visionResult.planarLocationOf(center)

			#Find the normal vector of a long edge
			m = markers[0]
			self.facing = visionResult.planarDirectionOf(m.normal)
			if m.type == sr.MARKER_BUCKET_END:
				self.facing = self.facing.left_perpendicular()

			self.facing.normalize()


		def transform(self, matrix):
			self.center = matrix * self.center
			self.facing = matrix * self.facing

		@property
		def desirableRobotTargets(self, distance = 1):
			"""The positions which the robot could be driven to for optimal deployment of cubes"""
			return (
				self.center + self.facing * distance,
				self.center - self.facing * distance
			)

		def __repr__(self):
			return "<Bucket #%d at %s>" % (self.id, repr(self.center))
			

	def planarLocationOf(self, point):
		"""
		:rtype: :class:`pyeuclid.Point2`
		Project a :class:`pyeuclid.Point3` onto the plane of the arena
		"""
		return Point2(point.x, point.z)

	def planarDirectionOf(self, vector):
		"""
		:rtype: :class:`pyeuclid.Vector2`
		Project a :class:`pyeuclid.Vector3` onto the plane of the arena
		"""
		return Vector2(vector.x, vector.z)

	def __init__(self, visionResult):
		self.timestamp = visionResult.timestamp
		self.arena     = [self.ArenaMarker(self, m) for m in visionResult.arena]
		self.tokens    = []
		self.buckets   = []
		self.robots    = []

		tokenmarkers   = defaultdict(list)
		bucketmarkers  = defaultdict(list)
		robotmarkers   = defaultdict(list)

		for m in visionResult.tokens:
			tokenmarkers[m.code] += [m]

		for m in visionResult.bucketEnds + visionResult.bucketSides:
			bucketmarkers[m.code] += [m]

		for m in visionResult.robots:
			robotmarkers[m.code] += [m]

		for code, markers in tokenmarkers.iteritems():
			self.tokens += [ self.Token(self, code, markers) ]

		for code, markers in bucketmarkers.iteritems():
			self.buckets += [ self.Bucket(self, code, markers)]

		for code, markers in robotmarkers.iteritems():
			self.robots += [ self.Robot(self, markers)]

		self.tokens.sort(key=lambda m: abs(m.center))
	
	def arenaMarkerEnds(self):
		# This may be useful:
		# unzip = lambda zipped: (lambda *x: x)(*map(list,zip(*zipped)))
		return PointSet([
			point
			for marker in self.arena
			for point in (marker.left, marker.right)
		])


import sys

# Hack to make pickle work properly - http://stackoverflow.com/a/1948057
setattr(sys.modules[__name__], 'ArenaMarker', ProcessedVisionResult.ArenaMarker) 
setattr(sys.modules[__name__], 'Token', ProcessedVisionResult.Token) 
setattr(sys.modules[__name__], 'Robot', ProcessedVisionResult.Robot) 
setattr(sys.modules[__name__], 'Bucket', ProcessedVisionResult.Bucket) 