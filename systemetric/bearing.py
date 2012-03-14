import math

class Bearing(object):
    '''Stores an angle between -180 and 180 degrees'''
    def __init__(self, degrees = None, radians = None):
        if radians is not None and degrees is not None:
            raise ValueError("degrees and radians cannot both be set")

        if degrees is None:
            degrees = math.degrees(radians or 0)
            
        while degrees >= 180:
            degrees -= 360
        while degrees < -180:
            degrees += 360
        self.degrees = float(degrees)
  
    @property
    def radians(self):
        '''Get the angle in radians'''
        return math.radians(self.degrees)
    
    @classmethod
    def toPoint(cls, p):
        '''Get the bearing from the origin to a given point'''
        angle = math.atan2(p.x, p.y)
        return cls(radians=angle)
        
    ofVector = toPoint
    
    def __float__(self):
        '''Make it easy to use as a number'''
        return self.degrees
        
    def __add__(self, other):
        return Bearing(float(self) + float(other))
    def __radd__(self, other):
        return Bearing(float(self) + float(other))
    
    def __sub__(self, other):
        return Bearing(float(self) - float(other))  
    def __rsub__(self, other):
        return Bearing(float(other) - float(self))

    def __abs__(self):
        return abs(float(self))
        
    def __invert__(self):
        return Bearing(-self.degrees)
        
    def __repr__(self):
        return u"%.1f\u00B0".encode('utf-8') % (self.degrees)