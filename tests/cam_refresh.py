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

from sr import *
import time
import math
import systemetric

def main():
    res = (320, 240)
    R = systemetric.Robot()
    
    
   # markers = [marker for marker in allMarkers if marker.info.marker_type == MARKER_TOKEN] #getting the valid QR code
    while True:
        markers = R.see(res=res)
        if len(markers) != 0:
            break
        R.power.beep(440,1)
        
    for i in range(21,0,-1):
        R.turn(i)
        time.sleep(1)
        markers = R.see( res=(640, 360) )
        if len(markers) != 0:        #if there is A valid QR there...
            print "Found, speed of ",i
            R.power.beep([(440,1), (220,1)])
            break
    R.stop()
   