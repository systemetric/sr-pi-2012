from sr import *
import systemetric
from libs.pyeuclid import *
import math

MARKERS_POSITIONS = {
	0: Point2(0, 0),
	1: Point2(1, 0),
	4: Point2(2, 0),
	9: Point2(3, 0)
}
robotPosition = Point2(0, 0)

def main():
	R = systemetric.Robot()
	angle = 0
	distance = 0

	while True:
		markers = R.see(res = (1280, 1024))
		
		if markers:
			angle = markers[0].rot_y + markers[0].orientation.rot_y
			print markers[0].rot_y, markers[0].orientation.rot_y
			distance = markers[0].dist
			robotPosition = Point2(math.sin(angle) * distance, math.cos(angle) * distance)

			print 'pos:', robotPosition, 'angle:', angle
		else:
			print 'no markers'

		#print [m.orientation.rot_y for m in markers]
