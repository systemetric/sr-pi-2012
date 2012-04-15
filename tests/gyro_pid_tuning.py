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

from systemetric.gyrorobot import *
import time
from tests.gui.slider import * 

def main():
	R = GyroAndCompassRobot()
	R.gyro.calibrate()


	# R.gyro.startOffsetCalibration()
	# time.sleep(5)
	# R.gyro.stopOffsetCalibration()

	# R.gyro.startScaleCalibration()
	# print 'rotate the gyro 90 degrees'
	# time.sleep(5)
	# R.gyro.stopScaleCalibration(90)


	regulator = R.gyroRegulator
	regulator.kp  = 0
	regulator.ki = 0
	regulator.kd = 0
	regulator.target = 0

	speed = [0]
	
	def keypressed(self, event):
		if event.keyval == gtk.keysyms.Page_Up and speed[0] < 100:
			speed[0] += 10
		elif event.keyval == gtk.keysyms.Page_Down and speed[0] > -100:
			speed[0] -= 10
	

	window = PIDWindow(regulator, max = (50, 50, 50))
	window.connect("key_press_event", keypressed)
	window.runInBackground()

	regulator.enabled = True

	while True:
		R.speed = speed[0]