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
import systemetric.logs as logs
import time

class Lifter(MbedDevice):
	"""A class to control the tilting platform on which the cubes are stored"""
	LIFT_WAIT = 2
	"""A rough estimate of the time taken for the platform to rise"""

	def __init__(self, mbed = None):
		super(Lifter, self).__init__('L', mbed)

	@logs.to(logs.events)
	def up(self, wait=True):
		"""Lift the platform up, tipping off cubes"""
		self.request('u')

		if wait:
			time.sleep(Lifter.LIFT_WAIT)

	@logs.to(logs.events)
	def down(self, wait=True):
		"""Bring the platform back down, so that more can be picked up"""
		self.request('d')

		if wait:
			time.sleep(Lifter.LIFT_WAIT)

	def wobble(self):
		"""Bring the platform up and down, to try and dislodge cubes"""
		self.up()
		time.sleep(1)
		self.down(wait=False)
		time.sleep(1)
		self.up(wait=False)
		time.sleep(1)
		self.down(wait=False)

def main():
	l = Lifter()

	l.up()
	l.down()
