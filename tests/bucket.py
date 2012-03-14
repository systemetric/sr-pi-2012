import systemetric
import time
from systemetric import Bearing
from systemetric.vision import ProcessedVisionResult
from libs.pyeuclid import *

R = systemetric.Robot()

STEPDIST = 1
try:
	while True:
		markers = R.see().processed()
		buckets = markers.buckets

		if buckets:
			b = buckets[0]

			target = min(b.desirableRobotTargets, key=abs)

			if abs(target) < 0.1:
				#Nearly at the target, don't move any more
				angle = Bearing.ofVector(b.center)

				if abs(angle) > 5:
					#Need to turn a bit more to face the bucket
					R.rotateBy(angle)

				#Angle is ok now - go for it!
				R.drive(15)
				time.sleep(1)
				R.stop()
				break;

			else:
				if abs(target) > STEPDIST:
					#Too far from target - try and get closer
					R.turnToFace(target)
					R.driveDistance(STEPDIST)

				else:
					#One more movement
					R.driveTo(target)
					time.sleep(0.1)

				#Turn to face where we think the bucket should be, so we can see it next loop
				targetFacing = b.center - target
				angleDifference = Bearing.ofVector(targetFacing) - Bearing.ofVector(target)
				R.rotateBy(angleDifference)
				R.stop()
			
		time.sleep(1)
		R.rotateBy(20)

		R.stop()

	R.power.beep(440, 1)

except:
	R.stop()