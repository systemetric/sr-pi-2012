import systemetric
from systemetric.mapping.arenamaps import S007SmallArenaMap

def main():
	R = systemetric.Robot()
	arenaMap = S007SmallArenaMap()
	while True:
		markers = R.see().processed()
		#print markers.tokens
		#print len(markers), markers
		if markers.arena:
			print markers.arenaMarkerEnds()
			print "Position", arenaMap.estimatePositionFrom(markers)
			#print "==========="
