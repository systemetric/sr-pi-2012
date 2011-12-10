from libs.pyeuclid import *
import systemetric

marker_width = (10/12.0) *0.25

class ArenaMarker(object):
	def __init__(center, zone):
		self.center = center
		self.zone = zone

		if zone == 0:
			side = Vector2(marker_width/2, 0)
		elif zone == 1:
			side = Vector2(0, marker_width/2)
		elif zone == 2:
			side = Vector2(-marker_width/2, 0)
		elif zone == 3:
			side = Vector2(0, -marker_width/2)

		self.left, self.right = center + side, center - side

arena = {
	0: ArenaMarker(Point2(1, 0), 0),
	1: ArenaMarker(Point2(2, 0), 0),
	2: ArenaMarker(Point2(3, 0), 0),
	3: ArenaMarker(Point2(4, 0), 0),
	4: ArenaMarker(Point2(5, 0), 0),
	5: ArenaMarker(Point2(6, 0), 0),
	6: ArenaMarker(Point2(7, 0), 0),

	7: ArenaMarker(Point2(8, 1), 1),
	8: ArenaMarker(Point2(8, 2), 1),
	9: ArenaMarker(Point2(8, 3), 1),
	10: ArenaMarker(Point2(8, 4), 1),
	11: ArenaMarker(Point2(8, 5), 1),
	12: ArenaMarker(Point2(8, 6), 1),
	13: ArenaMarker(Point2(8, 7), 1),

	14: ArenaMarker(Point2(7, 8), 2),
	15: ArenaMarker(Point2(6, 8), 2),
	16: ArenaMarker(Point2(5, 8), 2),
	17: ArenaMarker(Point2(4, 8), 2),
	18: ArenaMarker(Point2(3, 8), 2),
	19: ArenaMarker(Point2(2, 8), 2),
	20: ArenaMarker(Point2(1, 8), 2),

	21: ArenaMarker(Point2(0, 7), 3),
	22: ArenaMarker(Point2(0, 6), 3),
	23: ArenaMarker(Point2(0, 5), 3),
	24: ArenaMarker(Point2(0, 4), 3),
	25: ArenaMarker(Point2(0, 3), 3),
	26: ArenaMarker(Point2(0, 2), 3),
	27: ArenaMarker(Point2(0, 1), 3)
}

def positionsFromCodes(codes):
	positions = []
	for code in codes:
		pos = arena[code]
		positions += [pos.right, pos.left]
	return positions

def main():
	R = systemetric.Robot()
	while True:
		markerIds = []
		markers = R.see()
		for marker in markers.arena:
			markerIds += [marker.info.offset]

		actual = positionsFromCodes(markerIds)
		apparent = visionResult.arenaMarkerEdges()

		print "actual", actual
		print "apparent", apparent
		print actual.bestTransformTo(apparent)