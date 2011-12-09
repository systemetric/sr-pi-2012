import math
from libs.pyeuclid import *

class PointSet(list):
	MAX_PRECISION = 360

	def __init__(self, points):
		self[:] = points
		self._centered = None
		self._center = None

	def errorTo(self, other):
		"""Calculate the sum of the squares of the error between two list of points"""
		return sum((a - b).magnitude_squared() for a, b in zip(self, other))

	@property
	def center(self):
		"""Calculate the geometric center of the points"""
		if not self._center:
			self._center = sum(self, Vector2()) / float(len(self))

		return self._center

	@property
	def centered(self):
		"""Center all the points around the origin"""
		if not self._centered:
			self._centered = PointSet([p - self.center for p in self])
		
		return self._centered

	def transformedBy(self, matrix):
		"""Transform every point in this set by a matrix"""
		return PointSet([matrix * p for p in self])

	def bestTransformTo(self, other):
		"""Find the matrix transformation which best maps this point set onto another"""
		tried = []

		#Try `maxPrecision` rotations, in equal steps
		for i in range(PointSet.MAX_PRECISION):
			theta = i * math.pi * 2 / PointSet.MAX_PRECISION
			rotation = Matrix3.new_rotate(theta)
			
			e = self.centered.transformedBy(rotation).errorTo(other.centered)

			tried.append((rotation, e))

		rotation, error = min(tried, key=lambda x: x[1])

		#Add back on the translation components
		transform = Matrix3.new_translate(*other.center.xy) * rotation * Matrix3.new_translate(*self.center.xy).inverse()

		return (transform, error)

def tryIt():
	originalTransform = Matrix3.new_translate(5, 2) * Matrix3.new_rotate(math.pi/5) * Matrix3.new_translate(2, 6)

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

tryIt()