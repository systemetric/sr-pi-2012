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
import systemetric

def main():
	R = systemetric.Robot()
	while True:
		print "Reading markers"
		#Get only the tokens
		arenaMarkers = R.see(res=(1280,1024)).processed().arena
		
		# Are there any tokens?
		if arenaMarkers:
			nearest = min(arenaMarkers, key=lambda m: abs(m.center))
			R.driveTo(nearest.center, gap=0.2)
		else:
			print "No Marker..."
			
			# Spin 30 degrees clockwise
			R.rotateBy(30, fromTarget=True)
			
			# Disable heading correction
			R.stop()