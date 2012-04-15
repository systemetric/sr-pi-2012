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

import systemetric
from systemetric.mapping.arenamaps import *
from systemetric.map import Map
import time

def main():
	def grabCube():
		R.power.beep(440, 1)
		time.sleep(1)
		R.power.beep(880, 1)
		time.sleep(1)
		R.power.beep(440, 1)
		time.sleep(1)

	def driveTowards(relativeLocation, token):
		"""Drive at most 1 meter towards a cube. Return True if the cube was reached"""
		R.turnToFace(relativeLocation)
		distance = abs(relativeLocation)

		ROBOT_SIZE = 0.2

		if distance < ROBOT_SIZE:
			print "Found %s" % token
			return True

		elif distance > 1 + ROBOT_SIZE:
			print "More than 1m from %s" % token
			R.driveDistance(1)
			return False
		else:
			print "Less than 1m from %s" % token
			R.driveDistance(distance - ROBOT_SIZE + 0.05)
			return False

	gameMap = Map(arena=S007ArenaMap())

	R = systemetric.Robot()
	startTime = time.time()

	while True:
		print
		print time.time() - startTime
		vision = R.see().processed()

		gameMap.updateEntities(vision)

		if gameMap.robot:
			print "Robot at", gameMap.robot.location
			
			distanceTo = {}

			knownTokens = filter(lambda i: i.exists, gameMap.tokens)
			print gameMap.tokens

			if knownTokens:
				for entity in knownTokens:
					distanceTo[entity] = entity.position - gameMap.robot.location

				nearestToken = min(distanceTo, key = lambda e: abs(distanceTo[e]))

				print "Nearest marker is #%s at %s" % (nearestToken.id, nearestToken.position)

				vectorToCube = gameMap.robot.transform.inverse() * distanceTo[nearestToken]

				gotCube = driveTowards(vectorToCube, nearestToken)
				if gotCube:
					grabCube()
					nearestToken.invalidate()
				else:
					gameMap.invalidateRobotPosition()
			else:
				print "No tokens found"
				print "Spin on spot"
				#no tokens yet!
				R.rotateBy(40)
				R.stop()
		else:
			print "I'm lost!"
			print "Spin on spot"
			#no tokens yet, and I'm lost!
			R.rotateBy(40)
			R.stop()
			
		time.sleep(0.25)
