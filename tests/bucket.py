# This file is part of systemetric-student-robotics.

# systemetric-student-robotics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# systemetric-student-robotics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with systemetric-student-robotics.  If not, see <http://www.gnu.org/licenses/>.

import systemetric
import time
from systemetric import Bearing
from systemetric.vision import ProcessedVisionResult
from libs.pyeuclid import *

R = systemetric.Robot()

#Distance between each step to move towards a bucket in meters
#(e.g. if 2 meter step, every 2 meters it will check location of bucket again)
STEPDIST = 1

while True:
	#Get markers seen and the buckets within those markers
	markers = R.see().processed()
	buckets = markers.buckets

	#If seen any buckets
	if buckets:
		#Take first bucket as target
		b = buckets[0]

		#Choose the best point on the bucket to align to
		target = min(b.desirableRobotTargets, key=abs)

		#Print information to read
		print "Bucket seen at %s" % b.center
		print "Driving to %s" % target

		#If very close to the target
		if abs(target) < 0.1:
			#Print nearly there and get angle to center of the bucket
			print "Nearly there"
			angle = Bearing.ofVector(b.center)

			#If angle is not aligned enough
			if abs(angle) > 5:
				#Turn a bit more to face the bucket and print how far off
				print "Off by %s" % angle
				R.rotateBy(angle)

			#Angle is ok now - go for it!
			print "Success!"
			R.drive(15)
			time.sleep(1)
			R.stop()
			time.sleep(10)

		else:
			if abs(target) > STEPDIST:
				#Too far from target - limit movement
				target = STEPDIST * target.normalize()

			#One more movement
			R.driveTo(target)
			time.sleep(0.1)

			#Turn to face where we think the bucket should be, so we can see it next loop
			targetFacing = b.center - target
			angleDifference = Bearing.ofVector(targetFacing) - Bearing.ofVector(target)
			print "Turning to face bucket again"
			R.rotateBy(angleDifference)
			R.stop()
		
	time.sleep(1)
	R.rotateBy(20)

	R.stop()

R.power.beep(440, 1)
