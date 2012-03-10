import systemetric
from systemetric.mapping.arenamaps import *
from systemetric.timer import Timer
import time

def printTokens(d):
	#Print out the location of ALL THE TOKENS
	print dict(map(
		lambda pair: (pair[0], pair[1].center),
		d.iteritems()
	))

def main():

	allTokens = {}

	arenaMap = S007ArenaMap()

	locationInfo = None

	R = systemetric.Robot()
	startTime = time.time()

	while True:
		with Timer("profiling") as t:
			times = {}
			print
			print time.time() - startTime

			vision, vt = R.see(stats=True)
			times["see"] = vt
			with t.event("processed"):
				vision = vision.processed()

			#print markers.tokens
			#print len(markers), markers
			with t.event("locationInfo"):
				locationInfo = arenaMap.getLocationInfoFrom(vision) or locationInfo

			if locationInfo:
				print "Robot at", locationInfo.location
				with t.event("transform"):
					for token in vision.tokens:
						#Transform the token to object space
						token.transform(locationInfo.transform)
						#Update its position
						allTokens[token.id] = token

				distanceTo = {}
				printTokens(allTokens)

				if allTokens:
					with t.event("distanceTo"):
						for id, token in allTokens.iteritems():
							distanceTo[id] = allTokens[id].center - locationInfo.location


					with t.event("nearestMarkerId"):
						nearestMarkerId = min(distanceTo, key = lambda x: abs(distanceTo[x]))
					with t.event("nearestMarker"):
						nearestMarker = allTokens[nearestMarkerId]
					print "Nearest marker is", nearestMarker

					with t.event("vectorToCube"):
						vectorToCube = locationInfo.transform.inverse() * distanceTo[nearestMarkerId]

					with t.event("turnToFace"):
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
			print times
