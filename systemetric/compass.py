from bearing import Bearing
from mbed import MbedDevice

class Compass(MbedDevice):
    def __init__(self, mbed = None):
        super(Compass, self).__init__('C', mbed)
        self.zeroOffset = Bearing(0)

    @property
    def absoluteHeading(self):
        '''Get the compass heading from the mbed, measured from due north'''
        heading = 'n/a'
        try:
            heading = self.request('h')
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
        self.request('c')
        
    def stopCalibration(self):
        self.request('c')