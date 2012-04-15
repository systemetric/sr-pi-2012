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
import systemetric
import time

class Arm(MbedDevice):
	"""
	A class to control the arm via the mbed. The arm has two control wires - a
	blue one, which causes the arm to move when pulled to 0V (through a FET),
	and a yellow one, which is pulled to 0V when the bottom limit switches are pressed.
	"""
	def __init__(self, mbed = None):
		super(Arm, self).__init__('A', mbed)

	def grabCube(self, wait = True):
		self.request('g') #grab
		startTime = time.time()
		while wait and not self.atBottom and time.time() - startTime < 5:
			time.sleep(0.1)

	@property
	def atBottom(self):
		"""Bottom limit switches pressed?"""
		return 'True' in self.request('b') #atBottom

	@property
	def atTop(self):
		"""Bottom limit switches pressed?"""
		return 'True' in self.request('t') #atBottom

def main():
	A = Arm()
	R = systemetric.Robot()
	
	while True:
		time.sleep(3)
		A.grabCube(wait=True)
