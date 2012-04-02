import systemetric
import time
from systemetric import Bearing
from systemetric.vision import ProcessedVisionResult
from libs.pyeuclid import *

R = systemetric.Robot()

STEPDIST = 1
while True:
	markers = R.see().processed()
	buckets = markers.buckets

	if buckets:
		b = buckets[0]

		target = min(b.desirableRobotTargets, key=abs)

		print "Bucket seen at %s" % b.center
		print "Driving to %s" % target

		if abs(target) < 0.1:
			#Nearly at the target, don't move any more
			print "Nearly there"
			angle = Bearing.ofVector(b.center)


			if abs(angle) > 5:
				#Need to turn a bit more to face the bucket
				print "Off by %s" % angle
				R.rotateBy(angle)

			#Angle is ok now - go for it!
			print "Success!"
			R.drive(15)
			time.sleep(1)
			R.stop()
			time.sleep(10)

		else:
			if abs(target) > STEPDIST:
				#Too far from target - limit movement
				target = STEPDIST * target.normalize()

			#One more movement
			R.driveTo(target)
			time.sleep(0.1)

			#Turn to face where we think the bucket should be, so we can see it next loop
			targetFacing = b.center - target
			angleDifference = Bearing.ofVector(targetFacing) - Bearing.ofVector(target)
			print "Turning to face bucket again"
			R.rotateBy(angleDifference)
			R.stop()
		
	time.sleep(1)
	R.rotateBy(20)

	R.stop()

R.power.beep(440, 1)
