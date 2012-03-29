import serial
from bearing import Bearing

class Compass(object):
    def __init__(self, port = '/dev/ttyACM0'):
        try:
            self.port = serial.Serial(port)
           # self.port.timeout = 0.25
            self.port.open()
        except Exception:
            raise Exception('Cannot connect to mbed')
        
        self.zeroOffset = Bearing(0)

    @property
    def absoluteHeading(self):
        '''Get the compass heading from the mbed, measured from due north'''
        heading = 'n/a'
        try:
            self.port.write('H')
            heading = self.port.readline()
            return Bearing(int(heading) / 10.0) #convert the int we get from the mbed into a float.
        except:
            print 'got [' + heading + '] from the compass. Not correct!'
            return Bearing(float('nan')) #return NaN, because we don't know the heading

    @property
    def heading(self):
        '''Get the compass heading from the mbed, relative to the offset'''
        return self.absoluteHeading - self.zeroOffset

    @heading.setter
    def heading(self, value):
        '''Set conceptual zero to the current heading'''
        self.zeroOffset = self.absoluteHeading - value

    def startCalibration(self):
        self.port.write('C')
        
    def stopCalibration(self):
        self.port.write('C')