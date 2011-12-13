import sr
from libs.pyeuclid import *
from mapping.pointset import PointSet
from collections import defaultdict

class VisionResult(list):
	class Marker(object):
		"""
		A generic marker class that converts important information from the camera to pyeuclid types
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
			self.normal = (
				self.vertices[2] - self.vertices[1]
			).cross(
				self.vertices[0] - self.vertices[1]
			).normalize()
		
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
		self[:] = rawmarkers
		self.tokens = []
		self.arena = []
		self.robots = []
		self.buckets = []
		self.worldTransform = worldTransform

		for marker in rawmarkers:
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
		return ProcessedVisionResult(self)

class ProcessedVisionResult(object):
	"""
	2d representation of what can be seen
	"""
	class ArenaMarker(object):
		def __init__(self, visionResult, marker):
			self.id = marker.code

			#Convert points to 2D, and find midpoints
			v = [visionResult.planarLocationOf(v) for v in marker.vertices]
			mid1 = (v[0] + v[1]) / 2.0
			mid2 = (v[1] + v[2]) / 2.0
			mid3 = (v[2] + v[3]) / 2.0
			mid4 = (v[3] + v[0]) / 2.0

			#distance between midpoints
			d1 = abs(mid1 - mid3)
			d2 = abs(mid2 - mid4)

			midpoints = (mid1, mid3) if d1 > d2 else (mid2, mid4)
			
			#Calculate sin(angle between edges[0], the origin, and edges[1])
			sinAngle = midpoints[0].left_perpendicular().dot(midpoints[1])

			if sinAngle > 0:
				#First point is to the left [CHECK!] of second point
				self.left = midpoints[0]
				self.right = midpoints[1]
			else:
				#First point is to the right [CHECK!] of second point
				self.left = midpoints[1]
				self.right = midpoints[0]

	class Token(object):
		SIZE = 0.1
		def __init__(self, visionResult, id, markers):
			self.id = id
			self.markers = markers
			center = sum(m.center - m.normal * self.SIZE / 2 for m in markers) / len(markers)
			self.center = planarLocationOf(center)

		def __repr__(self):
			return "<ProcessedVisionResult.Token #%d at %s>" % (self.code, repr(self.center))

	class Robot(object):
		def __init__(self, visionResult, markers):
			pass

	class Bucket(object):
		def __init__(self, visionResult, markers):
			pass

	def planarLocationOf(self, point):
		return Point2(point.x, point.z)

	def __init__(self, visionResult):
		self.arena = [self.ArenaMarker(self, m) for m in visionResult.arena]
		self.tokens = []

		tokenmarkers = defaultdict(list)

		for m in visionResult.tokens:
			tokenmarkers[m.code] += [m]
		
		print tokenmarkers

		for code, markers in tokenmarkers.iteritems():
			self.tokens += [ self.Token(self, code, markers) ]

		self.tokens.sort(key=lambda m: abs(m.center))
	
	def arenaMarkerEnds(self):
		return PointSet([
			point
			for marker in self.arena
			for point in (marker.left, marker.right)
		])