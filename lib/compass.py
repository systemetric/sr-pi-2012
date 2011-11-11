import serial
from lib.bearing import Bearing

class Compass(object):
    def __init__(self, port = '/dev/ttyACM0'):
        try:
            self.port = serial.Serial(port)
            self.port.timeout = 0.25
            self.port.open()
        except Exception, c:
            raise Exception('Cannot connect to mbed')

    @property
    def heading(self):
        '''Get the compass heading from the mbed'''
        self.port.write('H')
        heading = self.port.readline()
        if heading:
            return Bearing(int(heading) / 10.0) #convert the int we get from the mbed into a float.
        else:
            return Bearing(float('nan')) #return NaN, because we don't know the heading
    
    def startCalibration(self):
        self.port.write('C')
        
    def endCalibration(self):
        self.port.write('C')