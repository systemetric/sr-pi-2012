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
	allTokens = {}

	R = systemetric.Robot()
	arenaMap = S007ArenaMap()
	while True:
		vision = R.see().processed()
		#print markers.tokens
		#print len(markers), markers
		locationInfo = arenaMap.getLocationInfoFrom(vision)

		if locationInfo:
			print "at", locationInfo.location
			for token in vision.tokens:
				#Transform the token to object space
				token.transform(locationInfo.transform)
				#Update its position
				allTokens[token.id] = token

			distanceTo = {}
			
			if allTokens:
				for id, token in allTokens.iteritems():
					distanceTo[id] = allTokens[id].center - locationInfo.location

				nearestMarkerId = min(distanceTo, key = lambda x: abs(distanceTo[x]))
				print "Nearest marker is", allTokens[nearestMarkerId]

				vectorToCube = locationInfo.transform.inverse() * distanceTo[nearestMarkerId]
				R.turnToFace(vectorToCube)

				distance = abs(vectorToCube)

				if distance < 0.4:
					#found
					del allTokens[nearestMarkerId]

					R.power.beep(440, 1)
					time.sleep(1)
					R.power.beep(880, 1)
					time.sleep(1)
					R.power.beep(440, 1)
					time.sleep(1)
				elif distance > 1:
					R.driveDistance(1 - 0.3)
				else:
					R.driveDistance(distance - 0.3)
			else:
				#no tokens yet!
				R.rotateBy(40)
				R.stop()
		else:
			#no tokens yet, and I'm lost!
			R.rotateBy(40)
			R.stop()
			
		
