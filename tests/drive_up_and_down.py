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

from sr import *
import time
import math
import systemetric

def main():
    forward = True
    R = systemetric.Robot()
    initialAngle = R.compass.heading
    R.rotateTo(initialAngle)
    while True:
        R.driveDistance(1 if forward else -1)
        R.rotateBy(60, fromTarget=True)
        markers = R.see()
        R.rotateBy(60, fromTarget=True)
        markers = R.see()
        R.rotateBy(60, fromTarget=True)
        time.sleep(0.5)

        forward = not forward