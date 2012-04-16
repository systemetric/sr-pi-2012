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
	R = systemetric.Robot()
	
	speed = 50
	
	while True:
		#Get only the tokens
		markers = [marker for marker in R.see() if marker.info.marker_type == MARKER_TOKEN]
		
		if len(markers) != 0:
			print "Saw the marker"
			angle = markers[0].centre.polar.rot_y
			if math.fabs(angle) < 10:
				R.drive(speed)
			else:
				R.turn(angle)
				time.sleep(0.25)
				R.stop()
			
			print(angle)
		else:
			print "No marker"
			R.turn(5)
			time.sleep(0.25)
			R.stop()