import time
import math
from systemetric import Bearing
from libs.pyeuclid import Point2
from systemetric.mapping.arenamaps import CompetitionArenaMap
from systemetric.map import Map

class CompetitionRobot():
	def __init__(self, R, m):
		self.R = R
		self.map = m

	def findCubesForXSeconds(self, x):
		startTime = time.time()
		foundCubes = set()
		while time.time() - startTime < x:
			print "Reading tokens"
			markers = self.R.see(res=(1280,1024)).processed()
			tokens = markers.tokens

			if tokens:
				target = tokens[0]
				if abs(target.center) > 1:
					self.R.driveTo(target.center, gap=0.75)
				else:
					self.R.driveTo(target.center, gap=0.2)
					if target.id not in foundCubes:
						foundCubes.add(target.id)
					print "Found cube #%d" % target.id
					self.R.arm.grabCube(wait=True)
					time.sleep(1)
					self.R.driveDistance(-0.5)
			else:
				print "Found no tokens"
				self.R.rotateBy(30, fromTarget=True)
				self.R.stop()
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
				print "Found no buckets"
				self.R.rotateBy(30, fromTarget=True)
				self.R.stop()
		return False

	def driveBackToZone(self):
		pos = self.map.robot.location
		targetPos = Point2(4.0 + math.cos(self.R.zone * math.pi / 2) * 3.5, 4.0 + math.sin(self.R.zone * math.pi / 2) * 3.5)

		self.R.rotateBy(math.atan2(targetPos.y - pos.y, targetPos.x - pos.x))
		self.R.driveDistance(((pos.x - targetPos.x)**2 + (pos.y - targetPos.y)**2)**0.5)

def main(R):
	m = Map(arena=CompetitionArenaMap())
	robot = CompetitionRobot(R, m)
	found = robot.findCubesForXSeconds(120)
	robot.driveBackToZone()
	robot.findBucketForXSeconds(30)