from systemetric import robot
import time

R = Robot()

while True:
	markers = R.see()
	for m in markers:
		if m.info.marker_type == MARKER_BUCKET_SIDE:
			 R.driveTo(m.center, gap=0.2)
			 R.driveDistance(1)
	time.sleep(1)
	R.rotateBy(20)