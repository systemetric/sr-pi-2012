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

import sr
from libs.pyeuclid import *
from processedvisionresult import ProcessedVisionResult
import time
import sys


class VisionResult(list):
	"""
	The class returned by `systemetric.Robot.see`. Splits the markers seen by
	type, into `tokens`, `arena`, `robots`, and `buckets`, since that's how
	they're most useful. For backwards compatibility, continues to behave as a
	simple list	like the one returned by `sr.Robot.see

		>>> vr = R.see()
		>>> vr[0]
		<VisionResult.Marker (code=15, type=MARKER_ARENA, center=Point3(1.0, 0.1, 2.5))>
		>>> vr.tokens[0]
		<VisionResult.Marker (code=0, type=MARKER_TOKEN, center=Point3(0.0, 0.0, 1.5))>

	.. attribute:: tokens
	               arena
	               bucketEnds
	               bucketSides

	   :type: lists of :class:`Marker`
	   Markers, grouped by type

	.. attribute:: timestamp

		The time that the vision was captured

	"""
	class Marker(object):
		"""
		A generic marker class that converts important information from the
		sr geometry types to pyeuclid types

		
		.. attribute:: vertices
		   
		   :type: list of :class:`pyeuclid.Point3`

		.. attribute:: center

		   :type: :class:`pyeuclid.Point3`

		.. attribute:: code

		   :type: integer
		   The offset of the marker - 0 for first bucket, token, robot, etc

		.. attribute:: type

		   The type of marker: one of ``MARKER_TOKEN``, ``MARKER_ARENA``,
		   ``MARKER_ROBOT``, ``MARKER_BUCKET_END``, and ``MARKER_BUCKET_SIDE``

		.. attribute:: normal

		   :type: :class:`pyeuclid.Vector3`
		   The normal vector pointing out of the surface of the marker, a :class:`pyeuclid.Vector3`

		"""
		def __init__(self, visionResult, rawmarker):
			self.visionResult = visionResult
			#Convert coordinates of things to a useful form
			self.vertices     = [visionResult.trueLocationOf(v) for v in rawmarker.vertices]
			self.center       = visionResult.trueLocationOf(rawmarker.centre)

			#Copy across useful properties
			self.code         = rawmarker.info.offset
			self.type         = rawmarker.info.marker_type

			#Pick two arbitrary edges and calculate the normal vector
			edge1             = self.vertices[2] - self.vertices[1]
			edge2             = self.vertices[0] - self.vertices[1]
			self.normal       = edge1.cross(edge2).normalize()
		
		def __repr__(self):
			return "<VisionResult.Marker (code=%d, type=%s, center=%s)>" % (self.code, self.type, repr(self.center))

	def trueLocationOf(self, srpoint):
		"""
		Take a point of the datatype returned by sr code, convert it to a
		pyeuclid format, then correct for camera orientation

		:rtype: :class:`pyeuclid.Point3`
		"""
		point = Point3(srpoint.world.x, srpoint.world.y, srpoint.world.z)
		return self.worldTransform * point

	def __init__(self, rawmarkers, worldTransform = None):
		self.timestamp = time.time()
		self[:] = rawmarkers
		self.tokens = []
		self.arena = []
		self.robots = []
		self.bucketEnds = []
		self.bucketSides = []
		self.worldTransform = worldTransform or Matrix4()

		for marker in rawmarkers:
			#Promote the object to the new type
			marker = self.Marker(self, marker)
			type = marker.type
			
			# What type of marker is it?
			if type == sr.MARKER_TOKEN:
				self.tokens += [ marker ]
			elif type == sr.MARKER_ARENA:
				self.arena += [ marker ]
			elif type == sr.MARKER_ROBOT:
				self.robots += [ marker ]
			elif type == sr.MARKER_BUCKET_END:
				self.bucketEnds += [ marker ]
			elif type == sr.MARKER_BUCKET_SIDE:
				self.bucketSides += [ marker ]

	def processed(self):
		"""Process this vision result, into a ProcessedVisionResult"""
		return ProcessedVisionResult(self)


# Hack to make pickle work properly - http://stackoverflow.com/a/1948057
setattr(sys.modules[__name__], 'Marker', VisionResult.Marker) 