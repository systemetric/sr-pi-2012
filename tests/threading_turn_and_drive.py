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

import systemetric
import threading
import time


robot = systemetric.Robot
def main(R):
	def spin():
		R.takeControl()
		while True:
			R.rotateBy(20)
			time.sleep(1)

	def drive():
		R.takeControl()
		while True:
			R.drive(40)
			time.sleep(3)
			R.drive(-40)

	driveR  = threading.Thread(target = drive)
	spinR = threading.Thread(target = spin)

	driveR.start()
	time.sleep(10)
	R.takeControl()
	R.power.beep(261, 1)
	spinR.start()
