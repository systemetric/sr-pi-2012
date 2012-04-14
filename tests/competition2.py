import time
import math
from systemetric import Bearing
from libs.pyeuclid import Point2
from systemetric.mapping.arenamaps import CompetitionArenaMap
from systemetric.map import Map

class CompetitionRobot():
	'''second comp program. Uses the compass to find the zone and bucket'''
	def __init__(self, R, m):
		self.R = R
		self.map = m
		self.rotations = 0

	def findCubesForXSeconds(self, x):
		startTime = time.time()
		foundCubes = set()
		while time.time() - startTime < x:
			print "Reading tokens"
			markers = self.R.see(res=(1280,1024)).processed()
			tokens = markers.tokens

			if tokens:
				print "Found %d tokens, going for token #%d" % (len(tokens), tokens[0].id)
				self.rotations = 0
				target = tokens[0]
				if abs(target.center) > 1:
					print "Too far from target cube, driving closer"
					self.R.driveTo(target.center, gap=0.5)
				else:
					print "Homing in on target cube"
					self.R.driveTo(target.center, gap=0.2)
					if target.id not in foundCubes:
						print "Definitely a new cube"
						foundCubes.add(target.id)
					print "Found cube #%d" % target.id
					self.R.arm.grabCube(wait=True)
					self.R.driveDistance(-0.1)
					self.R.arm.grabCube(wait=True)
					time.sleep(0.5)
					self.R.driveDistance(-0.5)
			else:
				if self.rotations >= 12:
					self.R.driveDistance(1)
					self.rotations = 0
				else:
					print "Found no tokens"
					self.R.rotateBy(30, fromTarget=True)
					self.R.stop()
					self.rotations += 1
		return foundCubes

	def findBucketForXSeconds(self, x):
		startTime = time.time()
		while time.time() - startTime < x:
			print "Reading buckets"
			markers = self.R.see(res=(1280,1024)).processed()
			buckets = markers.buckets
			if buckets:
				target = buckets[0]
				drivingTo = min(target.desirableRobotTargets, key=abs)
				if abs(drivingTo) < 0.2:
					print "Nearly at a bucket"
					angle = Bearing.ofVector(target.center)

					if abs(angle) > 5:
						print "Off by %s" % angle
						self.R.rotateBy(angle)

					print "Found bucket"
					self.R.driveDistance(0.75)
					self.R.drive(15)
					time.sleep(1)
					self.R.stop()
					self.R.lifter.up()
					time.sleep(1)
					self.R.lifter.down()
					return True
				else:
					if abs(drivingTo) > 1:
						#Too far from target - limit movement
						drivingTo = 1 * drivingTo.normalize()

					#One more movement
					self.R.driveTo(drivingTo)
					time.sleep(0.1)

					#Turn to face where we think the bucket should be, so we can see it next loop
					targetFacing = target.center - drivingTo
					angleDifference = Bearing.ofVector(targetFacing) - Bearing.ofVector(drivingTo)
					print "Turning to face bucket again"
					self.R.rotateBy(angleDifference)
					self.R.stop()
			else:
				print "Found no buckets"
				self.R.rotateBy(-30, fromTarget=True)
				self.R.stop()
		return False

	def driveBackToZone(self):
		self.R.rotateTo(180)

		startTime = time.time()
		inZone = False
		while not inZone and time.time() - startTime < 10:
			self.R.driveDistance(0.5)
			vision = self.R.see(res=(1280, 1024)).processed()
			walls = vision.arena

			for wall in walls:
				if wall.id / 7 == self.R.zone:
					self.R.driveTo(wall.left, gap=0.1)
					self.R.driveDistance(-0.25)
					inZone = True
					break

		if not inZone:
			self.R.us.ping()
			self.R.driveDistance(self.R.us.front - 0.25)

def main(R):
	m = Map(arena=CompetitionArenaMap())
	robot = CompetitionRobot(R, m)
	found = robot.findCubesForXSeconds(5)
	robot.driveBackToZone()
	if not robot.findBucketForXSeconds(30):
		robot.driveBackToZone()
		R.lifter.up()
		time.sleep(1)
		R.lifter.down()
		R.stop()
