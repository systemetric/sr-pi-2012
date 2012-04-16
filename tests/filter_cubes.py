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
class RobotCube(object):
	def __init__(self):
		self.R = systemetric.Robot()
	
	def check(self):
		if self.R.getMarkersById().tokens:
			return 1
		else:
			return 0
			
	def shortestDistance(self):
		self.cubes = self.R.getMarkersById().tokens
		self.lengths = {}
		
		#Are there really going to be markers closer than 0?
		distance = 0
		nearest = None
		
		for tokenId, markers in cubes:
			self.lengths[tokenId] = markers[0].dist
			
			#Won't this find the furthest one?
			if self.lengths[tokenId] > distance:
				distance = self.lengths[tokenId]
				nearest = tokenId
				
		return nearest
		
	 def driveToCube(self, cube, iterate=10):
		 for i in range(iterate):
			 R.setSpeed(cubes[cube].dist/2)
			 wait(0.1)
			 R.setSpeed(0)
			 wait(0.1)
			 cube = self.shortestDistance()
			 angle = cubes[cube].rot_x
			 R.rotateBy(angle)