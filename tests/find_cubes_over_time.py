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