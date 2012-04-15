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
import logs
import time

class Lifter(MbedDevice):
	LIFT_WAIT = 2

	def __init__(self, mbed = None):
		super(Lifter, self).__init__('L', mbed)

	@logs.to(logs.events)
	def up(self, wait=True):
		self.request('u')

		if wait:
			time.sleep(Lifter.LIFT_WAIT)

	@logs.to(logs.events)
	def down(self, wait=True):
		self.request('d')

		if wait:
			time.sleep(Lifter.LIFT_WAIT)

	def wobble(self):
		self.up()
		self.down(wait=False)

def main():
	l = Lifter

	l.up()
	l.down()
