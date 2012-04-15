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

#Any found tokens
foundTokens = set()

R = systemetric.Robot()

#Distance to drive up to tokens
targetTokenDistance = 0.45

def findTokensForXSeconds(x):
	startTime = time.time()

	while time.time() - startTime < x:
		print "Reading markers"

		markers = R.see(res=(1280,1024)).processed()
		tokens = markers.tokens

		for token in tokens:
			if token.id in foundTokens:
				print "\tIgnoring found token: " + token.id
				continue
			if abs(token) < targetTokenDistance:
				foundTokens.add(token.id)
				#Grab token
				print "\tFound token: " + token.id
				R.power.beep(440, 1)
				time.sleep(1)
			else:
				R.driveTo(token.center, gap=targetTokenDistance)

		if not tokens:
			#Couldn't find any markers
			print "\tNo tokens found..."
			
			# Spin 30 degrees clockwise
			R.rotateBy(30, fromTarget=True)
			
			# Disable heading correction
			R.stop()

findTokensForXSeconds(30)