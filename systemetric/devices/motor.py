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

class Motor(MbedDevice):
	def __init__(self, mbed = None, id=0):
		super(Motor, self).__init__('M', mbed)
		self._id = id
	@property
	def target(self):
		self.request("p", _id)
	
	@target.setter	
	def target(self, power):
		self.request(str(self._id), str(power))

def main():
	m0 = Motor(id=0)
	m1 = Motor(id=1)

	m0.target = 100
	m1.target = 100
	time.sleep(2)
	
	m0.target = -60
	m1.target = 60
	time.sleep(1)
	
	m0.target = 100
	m1.target = 100
	time.sleep(2)
	
	m0.target = 0
	m1.target = 0
