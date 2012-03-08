import systemetric
from systemetric.mapping.arenamaps import *
import time

def printTokens(d):
	#Print out the location of ALL THE TOKENS
	print dict(map(
		lambda pair: (pair[0], pair[1].center),
		d.iteritems()
	))

def grabCube():
	R.power.beep(440, 1)
	time.sleep(1)
	R.power.beep(880, 1)
	time.sleep(1)
	R.power.beep(440, 1)
	time.sleep(1)

def main():
	allTokens = {}

	gameMap = Map(arena=S007ArenaMap())

	locationInfo = None


	R = systemetric.Robot()
	startTime = time.time()

	while True:
		print
		print time.time() - startTime
		vision = R.see().processed()

		#If there are tokens within a meter
		if vision.tokens and min(abs(t.center) for t in vision.tokens) < 1:
			#Drive towards them, pick them up, update map in background
			#gameMap.updateEntities(vision)
		else:
			if True: #we have moved
				gameMap.updateEntities(vision)
				#Recalculate our position
			else
				#No point updating map
				pass;

			#If we know the location of some tokens
			if gameMap.tokens:
				#find the nearest one
				#turn to face it
				#Resume loop, with cube now directly in front, ready to be picked up by next iteration
				#Keep track of what we should see, so we can remove it from the map if it is not there?
				pass



		# check for

		#print markers.tokens
		#print len(markers), markers
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
				R.turnToFace(vectorToCube)

				distance = abs(vectorToCube)

				ROBOT_SIZE = 0.4

				if distance < ROBOT_SIZE:
					print "Found %s" % nearestMarker
					del allTokens[nearestMarkerId]
					grabCube()
				elif distance > 1 + ROBOT_SIZE:
					print "More than 1m from %s" % nearestMarker
					R.driveDistance(1)
					locationInfo = None
				else:
					print "Less than 1m from %s" % nearestMarker
					R.driveDistance(distance - ROBOT_SIZE + 0.05)
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
