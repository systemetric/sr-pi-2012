import systemetric
from systemetric.mapping.arenamaps import *
import time

def printTokens(d):
	#Print out the location of ALL THE TOKENS
	print dict(map(
		lambda pair: (pair[0], pair[1].center),
		d.iteritems()
	))

def main():
	def grabCube():
		R.power.beep(440, 1)
		time.sleep(1)
		R.power.beep(880, 1)
		time.sleep(1)
		R.power.beep(440, 1)
		time.sleep(1)

	def driveTowards(relativeLocation):
		"""Drive at most 1 meter towards a cube. Return True if the cube was reached"""
		R.turnToFace(relativeLocation)
		distance = abs(relativeLocation)

		ROBOT_SIZE = 0.2

		if distance < ROBOT_SIZE:
			print "Found %s" % nearestMarker
			return True

		elif distance > 1 + ROBOT_SIZE:
			print "More than 1m from %s" % nearestMarker
			R.driveDistance(1)
			return False
		else:
			print "Less than 1m from %s" % nearestMarker
			R.driveDistance(distance - ROBOT_SIZE + 0.05)
			return False

	allTokens = {}

	arenaMap = S007ArenaMap()

	locationInfo = None

	R = systemetric.Robot()
	startTime = time.time()

	while True:
		print
		print time.time() - startTime
		vision = R.see().processed()

		locationInfo = arenaMap.getLocationInfoFrom(vision) or locationInfo

		if locationInfo:
			print "Robot at", locationInfo.location
			for token in vision.tokens:
				#Transform the token to object space
				token.transform(locationInfo.transform)
				#Update its position
				allTokens[token.id] = token

			distanceTo = {}
			printTokens(allTokens)

			if allTokens:
				for id, token in allTokens.iteritems():
					distanceTo[id] = allTokens[id].center - locationInfo.location

				nearestMarkerId = min(distanceTo, key = lambda x: abs(distanceTo[x]))
				nearestMarker = allTokens[nearestMarkerId]
				print "Nearest marker is", nearestMarker

				vectorToCube = locationInfo.transform.inverse() * distanceTo[nearestMarkerId]

				gotCube = driveTowards(vectorToCube)
				if gotCube:
					grabCube()
					del allTokens[nearestMarkerId]
				else:
					locationInfo = None
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
