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
from systemetric import Bearing
import time
from tests.gui.slider import * 

def main():
	R = CompassRobot()
	R.compass.heading = 0

	regulator = R.regulator
	regulator.kp = 0
	regulator.ki = 0
	regulator.kd = 0
	regulator.target = 0

	def keypressed(self, event):
		if event.keyval == gtk.keysyms.n:
			regulator.target = Bearing(0)
		elif event.keyval == gtk.keysyms.e:
			regulator.target = Bearing(90)
		elif event.keyval == gtk.keysyms.s:
			regulator.target = Bearing(180)
		elif event.keyval == gtk.keysyms.w:
			regulator.target = Bearing(270)
		elif event.keyval == gtk.keysyms.Page_Up and R.speed < 100:
			R.speed += 10
		elif event.keyval == gtk.keysyms.Page_Down and R.speed > -100:
			R.speed -= 10
	
	window = PIDWindow(regulator)
	window.connect("key_press_event", keypressed)
	window.runInBackground()


	regulator.enabled = True

	#for p in range(18, 25, 1):
	#	regulator.kp = p / 10.0
	#	print p / 10.0
	#	regulator.enabled = True
	#	time.sleep(5)
	#	regulator.enabled = False
	#	R.stop()
	#	time.sleep(1)