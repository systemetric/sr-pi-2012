import systemetric
import time
from systemetric.vision import ProcessedVisionResult
from libs.pyeuclid import *

R = systemetric.Robot()

while True:
	markers = R.see()
	for b in markers.processed().buckets:
		target = min(b.desirableRobotTargets(), key=abs)
		R.driveTo(target)
	time.sleep(1)
	R.rotateBy(20)
	R.stop()