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