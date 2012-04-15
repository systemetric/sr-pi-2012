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

R = systemetric.twowheeledrobot.TwoWheeledRobot()
A = systemetric.arm.Arm()

def waitForSignal(delay=0.1):
	while not A.atTop:
		pass
	while A.atTop:
		pass
	time.sleep(delay)

def main():
	print "Voltage before\tvoltage during\tMotor power"
	for i in xrange(0, 100, 10):
		waitForSignal()
		v = R.power.battery.voltage

		R.drive(speed=100)
		time.sleep(0.1)
		R.drive(speed=i)
		time.sleep(2.5)
		print "%.2f\t%2f\t%d" % (v, R.power.battery.voltage, i)
		time.sleep(2.5)
		R.stop()
