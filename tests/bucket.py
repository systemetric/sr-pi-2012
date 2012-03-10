import systemetric
import time
from systemetric.vision import ProcessedVisionResult

R = systemetric.Robot()

while True:
	markers = R.see()
	for m in markers.bucketSides:
		target = ProcessedVisionResult.planarLocationOf(
			None, m.center + m.normal * 0.5
		)
		R.driveTo(target)
	time.sleep(1)
	R.rotateBy(20)
	R.stop()