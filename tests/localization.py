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
	startTime = time.time()
	allTokens = {}

	R = systemetric.Robot()
	arenaMap = S007ArenaMap()
	while True:
		print
		print time.time() - startTime
		vision = R.see().processed()
		#print markers.tokens
		#print len(markers), markers
		locationInfo = arenaMap.getLocationInfoFrom(vision)

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
				R.turnToFace(vectorToCube)

				distance = abs(vectorToCube)

				ROBOT_SIZE = 0.4

				if distance < ROBOT_SIZE:
					print "Found %s" % nearestMarker
					#found
					del allTokens[nearestMarkerId]

					R.power.beep(440, 1)
					time.sleep(1)
					R.power.beep(880, 1)
					time.sleep(1)
					R.power.beep(440, 1)
					time.sleep(1)
				elif distance > 1 + ROBOT_SIZE:
					print "More than 1m from %s" % nearestMarker
					R.driveDistance(1)
				else:
					print "Less than 1m from %s" % nearestMarker
					R.driveDistance(distance - ROBOT_SIZE)
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
