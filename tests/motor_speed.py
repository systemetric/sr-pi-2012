import systemetric
import systemetric.logs as logs
import time

def main():
	R = systemetric.Robot()
	R.power.beep(440, 0.5);
	logs.roundStarted()
	for i in range(100):
		R.drive(steer = i, speed = 0, regulate = False)
		print >> logs.movement, "speed %d" % i
		time.sleep(0.5)

