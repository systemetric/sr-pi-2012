from sr import *
import systemetric
import time

R = systemetric.Robot()

while True:
	markers = R.see()
	for m in markers.bucketSides:
		if m == MARKER_BUCKET_SIDE:
			 R.driveTo(m.centre, gap=0.2)
			 R.driveDistance(1)
	time.sleep(1)
	R.rotateBy(20)
	R.stop()