# This file is part of systemetric-student-robotics.

# systemetric-student-robotics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# systemetric-student-robotics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with systemetric-student-robotics.  If not, see <http://www.gnu.org/licenses/>.

import time
import math
from systemetric import Bearing

class CompetitionRobot():
	'''second comp program. Uses the compass to find the zone and bucket'''
	def __init__(self, R):
		self.R = R
		self.rotations = 0
		self.R.lifter.down()

	def findNCubesForXSeconds(self, n, x):
		startTime = time.time()
		foundCubes = set()
		lastTokenId = None

		while len(foundCubes) < n and time.time() - startTime < x:
			print "Reading tokens"
			markers = self.R.see(res=(1280,1024)).processed()
			tokens = markers.tokens

			if lastTokenId in foundCubes:
				correspondingTokens = [t for t in tokens if lastTokenId == t.id]
				if correspondingTokens and abs(correspondingTokens[0].center) > 0.2:
					foundCubes.remove(lastTokenId)

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
						lastTokenId = target.id
						foundCubes.add(lastTokenId)
					print "Found cube #%d" % target.id

					self.R.arm.grabCube(wait=True)

					if not self.R.arm.atBottom:
						self.R.driveDistance(-0.25)
						
					time.sleep(1)
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

	def findCubesForXSeconds(self, x):
		startTime = time.time()

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

					print "Found cube #%d" % target.id

					self.R.arm.grabCube(wait=True)

					if not self.R.arm.atBottom:
						self.R.driveDistance(-0.25)
						
					time.sleep(1)
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

	def findBucketForXSeconds(self, x):
		startTime = time.time()
		while time.time() - startTime < x:
			print "Reading buckets"
			markers = self.R.see(res=(1280,1024)).processed()
			buckets = markers.buckets
			if buckets:
				target = buckets[0]
				drivingTo = min(target.desirableRobotTargets, key=abs)
				if abs(drivingTo) < 1:
					print "Nearly at a bucket"
					angle = Bearing.ofVector(target.center)

					if abs(angle) > 10:
						print "Off by %s" % angle
						self.R.rotateBy(angle)

					print "Found bucket"
					self.R.driveTo(target.center, speed=50)
					time.sleep(1)
					self.R.lifter.up()
					self.R.drive(30)
					time.sleep(1.5)
					self.R.stop()
					self.R.lifter.down()
					time.sleep(1)
					self.R.lifter.up()
					time.sleep(1)
					self.R.lifter.down()
					return True
				else:
					#One more movement
					self.R.driveTo(drivingTo)
					time.sleep(0.1)

					#Turn to face where we think the bucket should be, so we can see it next loop
					angle = Bearing.ofVector(target.center)
					print "Turning to face bucket again"
					self.R.rotateBy(angle - math.copysign(2, angle))
					self.R.stop()
			else:
				print "Found no buckets"
				self.R.rotateBy(60, fromTarget=True)
				self.R.stop()
		return False

	def driveBackToZone(self):
		self.R.rotateTo(math.copysign(180, self.R.compass.heading))

		inZone = False
		while not inZone:
			vision = self.R.see(res=(1280, 1024)).processed()
			walls = vision.arena

			for wall in walls:
				if wall.id / 7 == self.R.zone:
					self.R.driveTo(wall.left, gap=0.1)
					self.R.driveDistance(-0.25)
					inZone = True
					break
			if not inZone:
				self.R.rotateTo(math.copysign(180, self.R.compass.heading))
				self.R.driveDistance(1.5)

def main(R):
	robot = CompetitionRobot(R)
	R.waitForStart()
	robot.findNCubesForXSeconds(6, 110)
	#robot.findCubesForXSeconds(110)
	robot.driveBackToZone()
	robot.findBucketForXSeconds(20)
	robot.driveBackToZone()
	R.lifter.up()
	robot.R.driveDistance(-0.25)
	time.sleep(1)
	R.lifter.down()
	R.stop()
