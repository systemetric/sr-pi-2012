import sr
from libs.pyeuclid import *
from processedvisionresult import ProcessedVisionResult
import time

class VisionResult(list):
	"""
	The class returned by `systemetric.Robot.see`. Splits the markers seen by
	type, into `tokens`, `arena`, `robots`, and `buckets`, since that's how
	they're most useful. For backwards compatibility, continues to behave as a
	simple list	like the one returned by `sr.Robot.see`
	"""
	class Marker(object):
		"""
		A generic marker class that converts important information from the
		sr geometry types to pyeuclid types
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
		"""
		point = Point3(srpoint.world.x, srpoint.world.y, srpoint.world.z)
		return self.worldTransform * point

	def __init__(self, rawmarkers, worldTransform = Matrix4()):
		self.timestamp = time.time()
		self[:] = rawmarkers
		self.tokens = []
		self.arena = []
		self.robots = []
		self.buckets = []
		self.worldTransform = worldTransform

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
			elif type == sr.MARKER_BUCKET:
				self.buckets += [ marker ]

	def processed(self):
		"""Process this vision result, into a ProcessedVisionResult"""
		return ProcessedVisionResult(self)

