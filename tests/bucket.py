import systemetric
import time
from systemetric.vision import ProcessedVisionResult
from pyeuclid import *

R = systemetric.Robot()

def planarLocationOf(self, point):
	return Point2(point.x, point.z)

while True:
	markers = R.see()
	for m in markers.bucketSides:
		target = planarLocationOf(m.center + m.normal * 0.5)
		R.driveTo(target)
	time.sleep(1)
	R.rotateBy(20)
	R.stop()