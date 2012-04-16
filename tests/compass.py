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
import threading

from systemetric import Robot

class CompassThread(threading.Thread):
	def __init__(self, robot):
		threading.Thread.__init__(self)
		self.R = robot
		self.target = 0
		self.speed = 0
		self.running = True
		
	def run(self):
		while self.running:
			heading = self.R.compass.heading
			error = float(self.target - heading)
			
			self.R.drive(speed = self.speed, steer = error/2)

def main():
	R = Robot()
	t = CompassThread(R)
	t.start()
	
	
	t.target = 0
	time.sleep(2.5)
	
	t.speed = 25
	time.sleep(1)
	t.speed = 0
	
	t.target = 90
	time.sleep(2.5)
	
	t.speed = 25
	time.sleep(1)
	t.speed = 0
	
	t.target = 180
	time.sleep(2.5)
	
	t.speed = 25
	time.sleep(1)
	t.speed = 0
	
	t.target = 270
	time.sleep(2.5)
	
	t.speed = 25
	time.sleep(1)
	t.speed = 0
	
	t.target = 0
	t.running = False
	t.join()
	R.stop()