import serial
from bearing import Bearing
from mbed import Mbed

class Compass(object):
    def __init__(self, mbed = None):
        self.mbed = mbed or Mbed.get()
        self.zeroOffset = Bearing(0)

    @property
    def absoluteHeading(self):
        '''Get the compass heading from the mbed, measured from due north'''
        heading = 'n/a'
        try:
            heading = self.mbed.sendCommand('H')
            return Bearing(int(heading) / 10.0) #convert the int we get from the mbed into a float.
        except:
            print 'got [' + heading + '] from the compass. Not correct!'
            return Bearing(float('nan')) #return NaN, because we don't know the heading

    @property
    def heading(self):
        '''Get the compass heading from the mbed, relative to the offset'''
        return self.absoluteHeading - self.zeroOffset

    def initializeZeroOffset(self):
        '''Set conceptual zero to the current heading'''
        self.zeroOffset = self.absoluteHeading

    def startCalibration(self):
        self.mbed.sendCommand('C')
        
    def stopCalibration(self):
        self.mbed.sendCommand('C')