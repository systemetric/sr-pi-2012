import systemetric
import time
from systemetric.vision import ProcessedVisionResult
from libs.pyeuclid import *

R = systemetric.Robot()

while True:
	markers = R.see()
	for b in markers.processed().buckets:
		target = min(b.desirableRobotTargets, key=abs)
		targetFacing = b.center - target
		R.driveTo(target)
		time.sleep(0.2)
		
		angleDifference = Bearing.ofVector(targetFacing) - Bearing.ofVector(target)
		R.rotateBy(angleDifference)
		R.stop()
		time.sleep(0.2)
		
		R.drive(15)
		time.sleep(1)
		R.stop()

	time.sleep(1)
	R.rotateBy(20)

	R.stop()