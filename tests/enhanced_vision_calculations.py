import systemetric
from systemetric.mapping.arenamaps import S007ArenaMap

def main():
	R = systemetric.Robot()
	arenaMap = S007ArenaMap()
	while True:
		markers = R.see().processed()
		#print markers.tokens
		#print len(markers), markers
		if markers.arena:
			print arenaMap.estimatePositionFrom(markers)
			#print "==========="
