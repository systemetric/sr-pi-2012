from libs.pyeuclid import *
from mapping.pointset import PointSet
from collections import defaultdict

class ProcessedVisionResult(object):
	"""
	2d representation of what can be seen
	"""
	class ArenaMarker(object):
		"""
		A marker around the walls of the arena. Extracts information about the
		left and right edge of the marker
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
		pushing the normal vector of each surface back inside the cube
		"""
		SIZE = 0.1
		def __init__(self, visionResult, id, markers):
			self.id = id
			self.markers = markers
			center = sum(m.center - m.normal * self.SIZE / 2 for m in markers) / len(markers)
			self.center = visionResult.planarLocationOf(center)

		def transform(self, matrix):
			self.center = matrix * self.center;

		def __repr__(self):
			return "<Token #%d at %s>" % (self.id, repr(self.center))

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

		for code, markers in tokenmarkers.iteritems():
			self.tokens += [ self.Token(self, code, markers) ]

		self.tokens.sort(key=lambda m: abs(m.center))
	
	def arenaMarkerEnds(self):
		# This may be useful:
		# unzip = lambda zipped: (lambda *x: x)(*map(list,zip(*zipped)))
		return PointSet([
			point
			for marker in self.arena
			for point in (marker.left, marker.right)
		])
