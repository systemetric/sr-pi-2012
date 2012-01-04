import systemetric
import time

def main():
	R = systemetric.Robot()
	#Forward
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise
	R.rotateBy(90)
	time.sleep(0.5)

	#Down
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise
	R.rotateBy(90)
	time.sleep(0.5)

	#Left
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise
	R.rotateBy(90)
	time.sleep(0.5)

	#Up
	R.drive(100)
	time.sleep(0.5)
	#Turn 90 clockwise back to regular position
	R.rotateBy(90)
	time.sleep(0.5)