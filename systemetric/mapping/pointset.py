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
		"""
		:arg :class:`PointSet` other: the points to compare to
		Calculate the sum of the squares of the distances between two list of points

		.. note::

			:arg:other must be of the same length as the object
		"""
		return sum((a - b).magnitude_squared() for a, b in zip(self, other))

	@property
	def center(self):
		"""
		:type: :class:`Point2`
		Calculate the geometric center of the points
		"""
		if not self.__center:
			self.__center = sum(self, Vector2()) / float(len(self))

		return self.__center

	@property
	def centered(self):
		"""
		:type: :class:`PointSet`
		A copy of the pointset with all the points centered around the origin
		"""
		if not self.__centered:
			self.__centered = PointSet([p - self.center for p in self])
		
		return self.__centered

	def transformedBy(self, matrix):
		"""
		:type: :class:`PointSet`
		A copy of the pointset with every point transformed by a matrix
		"""
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

		#Here be dragons
		optimalTheta = math.atan2(-e90, -e0)

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