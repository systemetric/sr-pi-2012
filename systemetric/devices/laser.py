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

class LaserGate(MbedDevice):
	"""
	A class to read the laser light gate via the mbed. The laser needs to be
	powered with 3.3V from the mbed, and some kind of light detector should be
	hooked up as well. Might be a good idea to only turn the laser on when the
	sensor is checked.
	"""
	def __init__(self, mbed = None):
		super(LaserGate, self).__init__('L', mbed)

	@property
	def blocked(self):
		return bool(self.request())
		#TODO: Maybe have the mbed return a float so that this code can decide
		#      what the definition of "blocked" is
