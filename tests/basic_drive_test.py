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
import time

def main():
	R = systemetric.Robot()
	#Forward
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise
	R.rotateBy(90)
	time.sleep(0.5)

	#Down
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise
	R.rotateBy(90)
	time.sleep(0.5)

	#Left
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise
	R.rotateBy(90)
	time.sleep(0.5)

	#Up
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise back to regular position
	R.rotateBy(90)
	time.sleep(0.5)