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

from systemetric.bearing import Bearing
from mbed import MbedDevice

class Compass(MbedDevice):
	'''A class to communicate with the compass via the mbed'''
	def __init__(self, mbed = None):
		super(Compass, self).__init__('C', mbed)
		self.zeroOffset = Bearing(0)

	@property
	def absoluteHeading(self):
		'''
		Get the compass heading from the mbed, measured from due north. Returns
		NaN upon error
		'''
		heading = 'n/a'
		try:
			heading = self.request('h')
			#convert the int we get from the mbed into a float
			return Bearing(int(heading) / 10.0) 
		except:
			print 'got [' + heading + '] from the compass. Not correct!'
			#return NaN, because we don't know the headin
			return Bearing(float('nan'))

	@property
	def heading(self):
		'''
		Get the compass heading from the mbed, relative to the offset. Returns
		NaN upon error.

		When set, adjusts the zero calibration of the compass such that an
		immediate read of `heading` gives the same value as it was set to
		'''
		return self.absoluteHeading - self.zeroOffset

	@heading.setter
	def heading(self, value):
		'''Set conceptual zero to the current heading'''
		self.zeroOffset = self.absoluteHeading - value

	def startCalibration(self):
		'''
		Start calibrating the compass. While this is happenning, the compass
		should be spun around slowly for two revolutions, taking about 20
		seconds
		'''
		self.request('c')
		
	def stopCalibration(self):
		'''Exit calibration mode'''
		self.request('c')

def main():
	import time
	comp = Compass()

	while True:
		time.sleep(0.5)
		print 'absolute heading: %f' % comp.absoluteHeading
		print 'heading: %f' % comp.heading
