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

from mbed import MbedDevice

class Ultrasonic(MbedDevice):
	"""
	A class for the four ultrasound sensors which were going to be attached
	to the mbed. Only one was attached, and it was not used in the competition
	"""
	def __init__(self, mbed = None):
		super(Ultrasonic, self).__init__('U', mbed)
		self.distances = [float("nan")] * 4  

	def ping(self):
		"""
		Ping the sensors, updating the :attr:`front`, :attr:`back`,
		:attr:`right`, and :attr:`left` properties
		"""
		self.distances = map(float, self.request().split())

	@property
	def front(self):
		"""The distance in meters to an obstacle in front"""
		return self.distances[0]
	
	@property
	def back(self):
		"""The distance in meters to an obstacle behind"""
		return self.distances[1]
	
	@property
	def left(self):
		"""The distance in meters to an obstacle to the left"""
		return self.distances[2]
	
	@property
	def right(self):
		"""The distance in meters to an obstacle to the right"""
		return self.distances[3]

def main():
	U = Ultrasonic()
	while True:
		U.ping()
		print U.front, U.back, U.left, U.right