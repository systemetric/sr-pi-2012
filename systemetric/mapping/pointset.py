import math
from libs.pyeuclid import *

class PointSet(list):
	"""
	A class to store a set of Point2s, adding useful methods. The array should
	_not_ be modified, as information is cached
	"""

	def __init__(self, points):
		"""Create a PointSet from an existing list of Point2s"""
		if len(points) == 0:
			raise ValueError("That set is empty!")

		self[:] = points
		self.__centered = None
		self.__center = None

	def errorTo(self, other):
		"""Calculate the sum of the squares of the error between two list of points"""
		return sum((a - b).magnitude_squared() for a, b in zip(self, other))

	@property
	def center(self):
		"""Calculate the geometric center of the points"""
		if not self.__center:
			self.__center = sum(self, Vector2()) / float(len(self))

		return self.__center

	@property
	def centered(self):
		"""Center all the points around the origin"""
		if not self.__centered:
			self.__centered = PointSet([p - self.center for p in self])
		
		return self.__centered

	def transformedBy(self, matrix):
		"""Transform every point in this set by a matrix"""
		return PointSet([matrix * p for p in self])

	"""Some prebuilt matrices for private use"""
	__rotate90 = Matrix3.new_rotate(math.pi/2)
	__rotate180 = Matrix3.new_scale(-1, -1)

	def bestTransformTo(self, other):
		"""
		Use a super-optimal method, since error as a function of rotation was found to be of the form

		    f(theta) = offset - amplitude * cos(theta - optimalTheta)
		
		through testing, and them some logical thought
		"""
		#Error upon rotating by 0, 90, and 180 degrees
		e0   = (self.centered).errorTo(other.centered)
		e90  = (self.centered.transformedBy(PointSet.__rotate90)).errorTo(other.centered)
		e180 = (self.centered.transformedBy(PointSet.__rotate180)).errorTo(other.centered)

		#Sum two points in antiphase, and the sine waves cancel, leaving twice the offset
		offset = (e0 + e180) / 2

		#remote the offsets - e180 not used any more
		e0  -= offset
		e90 -= offset

		#Pythagorean distance between two points 90 degrees out of phase is the amplitude
		amplitude = math.sqrt(e0**2 + e90**2)

		#             r0 = -amplitude * cos(-optimalTheta)
		#                = -amplitude * cos(optimalTheta)
		#-r0 / amplitude = cos(optimalTheta)
		optimalTheta     = math.acos(-e0 / amplitude)

		transform = Matrix3.new_translate(*other.center.xy) \
		          * Matrix3.new_rotate(optimalTheta)        \
		          * Matrix3.new_translate(*self.center.xy).inverse()
		#angle, matrix, error
		return (optimalTheta, transform, offset - amplitude)

def main():
	originalTransform = Matrix3.new_translate(5, 2) * Matrix3.new_rotate(math.pi/3) * Matrix3.new_translate(2, 6)

	square = PointSet([
		Point2(0, 0),
		Point2(0, 2),
		Point2(1, 1),
		Point2(5, 0)
	])

	rotated30 = square.transformedBy(originalTransform)

	calculatedTransform = square.bestTransformTo(rotated30)

	print originalTransform
	print calculatedTransform