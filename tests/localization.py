import systemetric
from systemetric.mapping.arenamaps import *
import time

class Timer(object):
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, t, v, tb):
        self.time = time.time() - self.start
        return False

def printTokens(d):
	#Print out the location of ALL THE TOKENS
	print dict(map(
		lambda pair: (pair[0], pair[1].center),
		d.iteritems()
	))

def main():
	timer = Timer()

	allTokens = {}

	arenaMap = S007ArenaMap()

	locationInfo = None

	R = systemetric.Robot()
	startTime = time.time()

	while True:
		times = {}
		print
		print time.time() - startTime

		with timer:
			vision = R.see()
		times["see"] = timer.time
		with timer:
			vision = vision.processed()
		times["processed"] = timer.time

		#print markers.tokens
		#print len(markers), markers
		with timer:
			locationInfo = arenaMap.getLocationInfoFrom(vision) or locationInfo
		times["locationInfo"] = timer.time

		if locationInfo:
			print "Robot at", locationInfo.location
			with timer:
				for token in vision.tokens:
					#Transform the token to object space
					token.transform(locationInfo.transform)
					#Update its position
					allTokens[token.id] = token
			times["transform"] = timer.time

			distanceTo = {}
			printTokens(allTokens)

			if allTokens:
				with timer:
					for id, token in allTokens.iteritems():
						distanceTo[id] = allTokens[id].center - locationInfo.location
				times["distanceTo"] = timer.time


				with timer:
					nearestMarkerId = min(distanceTo, key = lambda x: abs(distanceTo[x]))
				times["nearestMarkerId"] = timer.time
				with timer:
					nearestMarker = allTokens[nearestMarkerId]
				times["nearestMarker"] = timer.time
				print "Nearest marker is", nearestMarker

				with timer:
					vectorToCube = locationInfo.transform.inverse() * distanceTo[nearestMarkerId]
				times["vectorToCube"] = timer.time

				with timer:
					R.turnToFace(vectorToCube)
				times["turnToFace"] = timer.time

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
