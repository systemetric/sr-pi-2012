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
	
	def keypressed(self, event):
		if event.keyval == gtk.keysyms.Page_Up and R.speed < 100:
			R.speed += 10
		elif event.keyval == gtk.keysyms.Page_Down and R.speed > -100:
			R.speed -= 10
	
	window = PIDWindow(regulator, max = (50, 50, 50))
	window.connect("key_press_event", keypressed)
	window.runInBackground()

	regulator.enabled = True