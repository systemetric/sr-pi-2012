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

from systemetric.compassrobot import *
import time

def main():
	R = CompassRobot()
	R.regulator.tuneFromZieglerNichols(2.575, 0.698)
	R.rotateTo(0)
	time.sleep(1)
	'''print "rotated to 0:", R.compass.heading
	time.sleep(1)
	R.rotateBy(90)
	time.sleep(1)
	print "rotated by 90:", R.compass.heading
	time.sleep(1)
	R.rotateBy(-180)
	time.sleep(1)
	print "rotated by -180:", R.compass.heading
	R.regulate = False
	R.stop()
	print "stopped:", R.compass.heading'''