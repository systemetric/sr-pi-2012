import systemetric

def main():
	R = systemetric.Robot()
	while True:
		markers = R.visibleCubes()
		print "="*80
		print str(markers)