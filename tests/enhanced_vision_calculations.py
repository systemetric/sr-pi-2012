import systemetric

def main():
	R = systemetric.Robot()
	assert 1 == 3
	while True:
		markers = R.see().processed()
		print markers.tokens
		#print len(markers), markers
		#print markers.arenaMarkerEdges()
		#print "==========="
