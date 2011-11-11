import math

class Bearing(object):
    '''Stores an angle between -180 and 180 degrees'''
    def __init__(self, angle):
        while angle >= 180:
            angle -= 360
        while angle < -180:
            angle += 360
        self.degrees = float(angle)
  
    @property
    def radians(self):
        '''Get the angle in radians'''
        return math.radians(self.degrees)
        
    def __float__(self):
        '''Make it easy to use as a number'''
        return self.degrees
        
    def __add__(self, other):
        return Bearing(float(self) + float(other))
        
    def __sub__(self, other):
        return Bearing(float(self) - float(other))
        
    def __repr__(self):
        return u"%.1f\u00B0".encode('utf-8')%(self.degrees)
    

# print Bearing(20)
# print Bearing(-20) - Bearing(20)