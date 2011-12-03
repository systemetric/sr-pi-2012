from sr import *
import systemetric
import time

def main():
	R = systemetric.Robot()
	speed = 25
	while True:
		R.rotateTo(0)
		R.drive(speed)
		time.sleep(1)