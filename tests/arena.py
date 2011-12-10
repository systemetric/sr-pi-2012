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
def positionFromMarkerPair(marker1, marker2):
	marker1Id = marker1.info.offset
	marker2Id = marker2.info.offset
	
def positionFromMarker(marker):
	markerId = marker.info.offset

	if markerPosition:
		angleSeenAt = marker.rot_y
		relativeRotation = marker.orientation.rot_y

		#In radians
		angle = math.radians(angleSeenAt + (90 - relativeRotation))

		#print "Angles: %.1f %.1f" % (angleSeenAt, relativeRotation)
		distance = marker.dist
		relativePosition = Point2(math.cos(angle) * distance, math.sin(angle) * distance)

		return relativePosition + markerPosition

def main():
	R = systemetric.Robot()

	while True:
		markers = R.see(res = (1280, 1024))
		print map(positionFromMarker, markers)
		"""
		if len(markers) == 1:
			positionFromMarker(markers[0])
		elif len(markers) > 1:
			print len(markers), 'markers'
		else:
			print 'no markers'
"""
		#print [m.orientation.rot_y for m in markers]
