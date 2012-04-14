import time
import math
from systemetric import Map
from systemetric import Bearing
from libs.pyeuclid import Point2

def findCubesForXSeconds(R, x):
	startTime = time.time()
	foundCubes = set()
	while time.time() - startTime < x:
		print "Reading tokens"
		markers = R.see(res=(1280,1024)).processed()
		tokens = markers.tokens

		if tokens:
			target = tokens[0]
			if abs(target.center) > 1:
				R.driveTo(target.center, gap=0.75)
			else:
				R.driveTo(target.center, gap=0.2)
				if target.id not in foundCubes:
					foundCubes.add(target.id)
				print "Found cube #%d" % target.id
				R.arm.grabCube(wait=True)
				time.sleep(1)
				R.driveDistance(-0.25)
		else:
			print "Found no tokens"
			R.rotateBy(30, fromTarget=True)
			R.stop()
	return foundCubes

def findBucketForXSeconds(R, x):
	startTime = time.time()
	while time.time() - startTime < x:
		print "Reading buckets"
		markers = R.see(res=(1280,1024)).processed()
		buckets = buckets.tokens
		if buckets:
			target = buckets[0]
			drivingTo = min(target.desirableRobotTargets, key=abs)
			if abs(drivingTo) < 0.2:
				print "Nearly at a bucket"
				angle = Bearing.ofVector(target.center)

				if abs(angle) > 5:
					print "Off by %s" % angle
					R.rotateBy(angle)

				print "Found bucket"
				R.driveDistance(0.75)
				R.drive(15)
				time.sleep(1)
				R.stop()
				R.lifter.up()
				time.sleep(1)
				R.lifter.down()
				return True
		else:
			print "Found no buckets"
			R.rotateBy(30, fromTarget=True)
			R.stop()
	return False

def driveBackToZone(R, m, num):
	pos = m.robot.location
	targetPos = Point2(4.0 + Math.cos(num * Math.pi / 2) * 3.5, 4.0 + Math.sin(num * Math.pi / 2) * 3.5)

	R.rotateBy(Math.atan2(targetPos.y - pos.y, targetPos.x - pos.x))
	R.driveDistance(((pos.x - targetPos.x)**2 + (pos.y - targetPos.y)**2)**0.5)

def main(R):
	m = Map(arena=CompetitionArenaMap())
	found = findCubesForXSeconds(R, 120)
	driveBackToZone(R, R.zone)
	findBucketForXSeconds(R, 30)
