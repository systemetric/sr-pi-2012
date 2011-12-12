import systemetric

def main():
	R = systemetric.Robot()
	while True:
		markers = R.see()
		print markers.arena
		#print len(markers), markers
		#print markers.arenaMarkerEdges()
		#print "==========="
