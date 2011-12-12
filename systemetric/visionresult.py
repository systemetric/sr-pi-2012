import sr
from libs.pyeuclid import *
from mapping.pointset import PointSet

class VisionResult(list):
	class Marker(object):
		"""
		A generic marker class that converts important information from the camera to pyeuclid types
		"""
		def __init__(self, visionResult, rawmarker):
			self.visionResult = visionResult
			self.vertices     = [Point3(v.world.x, v.world.y, v.world.z) for v in rawmarker.vertices]
			self.code         = rawmarker.info.offset
			self.location     = rawmarker.centre.world

			#Pick two arbitrary edges and calculate the normal vector
			edge1 = self.vertices[2] - self.vertices[1]
			edge2 = self.vertices[0] - self.vertices[1]
			self.normal = edge1.cross(edge2).normalize()

	class ArenaMarker(Marker):
		def __init__(self, visionResult, rawmarker):
			VisionResult.Marker.__init__(self, visionResult, rawmarker)

			#Projected corners
			corners = [visionResult.projectToFieldPlane(c) for c in self.vertices]

			#Midpoints of edges
			mid1 = (corners[0] + corners[1]) / 2.0
			mid2 = (corners[1] + corners[2]) / 2.0
			mid3 = (corners[2] + corners[3]) / 2.0
			mid4 = (corners[3] + corners[0]) / 2.0

			#distance between midpoints
			d1 = abs(mid1 - mid3)
			d2 = abs(mid2 - mid4)

			if d1 > d2:
				midpoints = (mid1, mid3)
			else:
				midpoints = (mid2, mid4)
			
			#Calculate sin(angle between edges[0], the origin, and edges[1])
			sinAngle = midpoints[0].left_perpendicular().dot(midpoints[1])

			if sinAngle > 0:
				#First point is to the left [CHECK!] of second point
				self.left = midpoints[0]
				self.right = midpoints[1]
			else:
				#First point is to the right [CHECK!] of second point
				self.left = midpoints
				[1]
				self.right = midpoints[0]

	class Token(object):
		SIZE = 0.1
		def __init__(self, markers):
			self.markers = markers
			self.center = sum(m.location - m.normal * SIZE / 2 for m in markers) / len(markers)			

	def __init__(self, rawmarkers, skip = ()):
		self[:] = rawmarkers
		self.tokens = []
		self.arena = []
		self.robots = []
		self.buckets = []
		self.cameraMatrix = Matrix4()
		#self.cameraMatrix = Matrix4.new_rotate_euler(	# https://github.com/dov/pyeuclid/blob/master/euclid.txt (line 385)
		#	heading = 0,								 # rotation around the y axis
		#	attitude = -5,							  # rotation around the x axis
		#	bank = 0									 # rotation around the z axis
		#)
		self.__groupByType(skip)

	def __groupByType(self, skip):
		'''Sub divides and processes the types of markers'''
		for marker in self:
			#id = marker.info.offset
			type = marker.info.marker_type
			
			# What type of marker is it?
			if type == sr.MARKER_TOKEN and 'tokens' not in skip:
				self.tokens += marker #[ Marker(marker) ] - Leave to prevent breakage of existing code
			elif type == sr.MARKER_ARENA and 'arena' not in skip:
				self.arena += [ self.ArenaMarker(self, marker) ]
			elif type == sr.MARKER_ROBOT and 'robots' not in skip:
				self.robots += [ self.Marker(self, marker) ]
			elif 'buckets' not in skip:
				self.buckets += [ self.Marker(self, marker) ]
			
			##Is this the first marker we've seen for this object?
			#if not id in list:
			#	list[id] = []
			

			#Add this marker to the list of markers for this object
			#list[id].append(marker)
			#list.append(marker)

	def projectToFieldPlane(self, point):
		return Point2(*(self.cameraMatrix * point).xz)
	
	def visibleCubes(self):		
		tokens = []
		estimatedCentres = []

		# For each token
		for markerId, markers in self.tokens.iteritems():
			newmarkers = []
			# Convert all the markers to a nicer format, using pyeuclid
			for marker in markers:
			
				vertices = []
				# We only care about 3D coordinates - keep those
				for v in marker.vertices:
					vertices.append(Point3(
						v.world.x,
						v.world.y,
						v.world.z
					))
				
				# Calculate the normal vector of the surface
				edge1 = vertices[2] - vertices[1]
				edge2 = vertices[0] - vertices[1]
				normal = edge1.cross(edge2).normalize()
				
				# Keep the center position
				location = marker.centre.world

				newmarkers.append(Marker(
					location = Point3(location.x, location.y, location.z),
					normal = normal,
					vertices = vertices
				))
				
				estimatedCentres.append(location - normal * 0.05)
			
			token = Token(
				markers = newmarkers,
				timestamp = markers[0].timestamp,
				id = markerId,
				location = sum(estimatedCentres) / len(estimatedCentres)
			)
			# Take into account the position of the robot
			# token.location = self.robotMatrix * token.Location
			tokens.append(token)
		
		#sort by distance, for convenience
		tokens.sort(key=lambda m: m.location.magnitude())
		return tokens


	def arenaMarkerEdges(self):
		edges = []
		for marker in self.arena:

			corners = [self.__convertPoint(v) for v in marker.vertices]

			#Midpoints of edges
			edge1 = (corners[0] + corners[1]) / 2.0
			edge2 = (corners[1] + corners[2]) / 2.0
			edge3 = (corners[2] + corners[3]) / 2.0
			edge4 = (corners[3] + corners[0]) / 2.0

			#Horizontal distance between midpoints
			d1 = (edge1 - edge3).x
			d2 = (edge2 - edge4).x

			if abs(d1) >= abs(d2):
				if d1 > 0:
					edges += [edge1, edge3]
				else:
					edges += [edge3, edge1]
			else:
				if d2 > 0:
					edges += [edge2, edge4]
				else:
					edges += [edge4, edge2]
					
		return PointSet([self.__projectToFieldPlane(edge) for edge in edges])

