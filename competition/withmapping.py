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
from libs.pyeuclid import Point2
from systemetric.mapping.arenamaps import CompetitionArenaMap
from systemetric.map import Map

class CompetitionRobot():
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
				print "Found no buckets"
				self.R.rotateBy(30, fromTarget=True)
				self.R.stop()
		return False

	def driveBackToZone(self):
		while not self.map.robot:
			self.map.updateEntities(self.R.see(res=(1280,1024)).processed())
		pos = self.map.robot.location
		targetPos = Point2(4.0 + math.cos(self.R.zone * math.pi / 2) * 3.5, 4.0 + math.sin(self.R.zone * math.pi / 2) * 3.5)

		self.R.rotateBy(math.atan2(targetPos.y - pos.y, targetPos.x - pos.x))
		self.R.driveDistance(((pos.x - targetPos.x)**2 + (pos.y - targetPos.y)**2)**0.5)

def main(R):
	m = Map(arena=CompetitionArenaMap())
	robot = CompetitionRobot(R, m)
	R.waitForStart()
	#found = robot.findCubesForXSeconds(0)
	robot.driveBackToZone()
	#xxrobot.findBucketForXSeconds(30)
