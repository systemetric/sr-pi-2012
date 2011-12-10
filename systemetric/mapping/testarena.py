from libs.pyeuclid import *
import systemetric

marker_width = (10/12.0) *0.25

def arenaPosition(center, zone):
	if zone == 0:
		side = Vector2(marker_width/2, 0)
		return (center - side, center + side)
	elif zone == 1:
		side = Vector2(0, marker_width/2)
		return (center - side, center + side)
	elif zone == 2:
		side = Vector2(marker_width/2, 0)
		return (center + side, center - side)
	elif zone == 3:
		side = Vector2(0, marker_width/2)
		return (center + side, center - side)

arena = {
	0: arenaPosition(Point2(1, 0), 0),
	1: arenaPosition(Point2(2, 0), 0),
	2: arenaPosition(Point2(3, 0), 0),
	3: arenaPosition(Point2(4, 0), 0),
	4: arenaPosition(Point2(5, 0), 0),
	5: arenaPosition(Point2(6, 0), 0),
	6: arenaPosition(Point2(7, 0), 0),

	7: arenaPosition(Point2(8, 1), 1),
	8: arenaPosition(Point2(8, 2), 1),
	9: arenaPosition(Point2(8, 3), 1),
	10: arenaPosition(Point2(8, 4), 1),
	11: arenaPosition(Point2(8, 5), 1),
	12: arenaPosition(Point2(8, 6), 1),
	13: arenaPosition(Point2(8, 7), 1),

	14: arenaPosition(Point2(7, 8), 2),
	15: arenaPosition(Point2(6, 8), 2),
	16: arenaPosition(Point2(5, 8), 2),
	17: arenaPosition(Point2(4, 8), 2),
	18: arenaPosition(Point2(3, 8), 2),
	19: arenaPosition(Point2(2, 8), 2),
	20: arenaPosition(Point2(1, 8), 2),

	21: arenaPosition(Point2(0, 7), 3),
	22: arenaPosition(Point2(0, 6), 3),
	23: arenaPosition(Point2(0, 5), 3),
	24: arenaPosition(Point2(0, 4), 3),
	25: arenaPosition(Point2(0, 3), 3),
	26: arenaPosition(Point2(0, 2), 3),
	27: arenaPosition(Point2(0, 1), 3)
}
def positionsFromCodes(codes):
	positions = []
	for code in codes:
		pos = arena[code]
		positions += pos
	return positions

def main():
	R = systemetric.Robot()
	while True:
		markerIds = []
		markers = R.see()
		for marker in markers.arena:
			markerIds += [marker.info.offset]
		print positionsFromCodes(markerIds)


	print arena