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
import time

class Gyro(MbedDevice):
	'''A class to communicate with the gyro via the mbed'''
	def __init__(self, mbed = None):
		super(Gyro, self).__init__('G', mbed)

	@property
	def angularVelocity(self):
		"""
		Get the angular velocity measured by the gyro. Approximately calibrated
		to degrees per second
		"""
		return float(self.request('v'))

	def calibrate(self):
		"""
		Calibrate the zero offset of the compass, by sampling and averaging a
		lot of readings. This should be called frequently, as the voltage
		supplied to the mbed appears to change, changing the response of the
		sensor.
		"""
		self.request('c')

def main():
	gyro = Gyro()
	gyro.calibrate()

	while 1:
		print "Angular Velocity:", gyro.angularVelocity
		time.sleep(0.1)