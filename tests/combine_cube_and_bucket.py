import systemetric
import time
from systemetric import Bearing

R = systemetric.Robot()

followState = "cube"
foundCubes = set()

STEPDIST = 1

while True:
	markers = R.see(res=(1280,1024)).processed()
	if followState == "cube":
		print "Reading markers"
		#Get only the tokens
		tokens = [m for m in markers.tokens if m.id not in foundCubes]
		
		# Are there any tokens?
		if tokens:
			if abs(tokens[0].center) < 0.45:
				foundCubes.add(tokens[0].id)
				print "Found cube #%d!" % tokens[0].id
				R.power.beep(440, 1)
				time.sleep(1)
			else:
				R.driveTo(tokens[0].center, gap=0.2)
		else:
			print "No Marker..."
			
			# Spin 30 degrees clockwise
			R.rotateBy(30, fromTarget=True)
			
			# Disable heading correction
			R.stop()

		if len(foundCubes) > 1:
			followState = "bucket"
			foundCubes = set()

	elif followState == "bucket":
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
				R.power.beep(440, 1)
				
				followState = "cube"
				continue

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