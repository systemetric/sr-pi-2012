from sr import *
import systemetric
from libs.pyeuclid import *
import math

MARKERS_POSITIONS = {
	9: Point2(0, 0),
	4: Point2(1, 0),
	0: Point2(2, 0)
}
robotPosition = Point2(0, 0)
def positionFromMarker(marker):
	markerId = marker.info.offset
	markerPosition = MARKERS_POSITIONS.get(markerId)
	if markerPosition:
		angleSeenAt = marker.rot_y
		relativeRotation = marker.orientation.rot_y

		#In radians
		angle = math.radians(angleSeenAt + (90 - relativeRotation))

		#print "Angles: %.1f %.1f" % (angleSeenAt, relativeRotation)
		distance = marker.dist
		robotPosition = Point2(math.cos(angle) * distance, math.sin(angle) * distance)

		print 'pos:', robotPosition + markerPosition, 'angle:', angle

def main():
	R = systemetric.Robot()

	while True:
		markers = R.see(res = (1280, 1024))
		print map(markers, positionFromMarker)
		"""
		if len(markers) == 1:
			positionFromMarker(markers[0])
		elif len(markers) > 1:
			print len(markers), 'markers'
		else:
			print 'no markers'
"""
		#print [m.orientation.rot_y for m in markers]
