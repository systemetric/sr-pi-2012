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

import time
from systemetric import Robot

def main():
    R = Robot()
    
    R.compass.startCalibration()
    R.turn(8)
    time.sleep(20)
    R.compass.stopCalibration()
    R.stop()
    while True:
        print "bearing " + str(R.compass.heading)
        time.sleep(0.1)