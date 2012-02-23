import systemetric
from systemetric.mapping.arenamaps import S007ArenaMap

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
			for token in vision.tokens:
				#Transform the token to object space
				token.transform(locationInfo.transform)
				#Update its position
				allTokens[token.id] = token

			distanceTo = {}
			
			if allTokens:
				for id, token in allTokens.iteritems():
					distanceTo[id] = allTokens[id].center - locationInfo.location

				nearestMarker = min(distanceTo, key = lambda x: abs(distanceTo[x]))
				print "Nearest marker is", allTokens[nearestMarker]
			
		#Print out the location of ALL THE TOKENS
		print dict(map(
			lambda pair: (pair[0], pair[1].center),
			allTokens.iteritems()
		))
