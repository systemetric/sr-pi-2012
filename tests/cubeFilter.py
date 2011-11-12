from sr import *
from lib.compass import Compass
from lib.systemetricRobot import SystemetricRobot
class RobotCube(object):
    def __init__(self):
        self.R = SystemetricRobot()
    
    def check(self):
        if self.R.getMarkersById().tokens:
            return 1
        else:
            return 0
    def shortestDistance(self)
        self.cubes = self.R.getMarkersById().tokens
        self.lengths = {}
        distance = 0
        value = ''
        for key, value in cubes:
            self.lengths[key] = value[0].dist
            if self.lengths[key] > distance:
                distance = self.lengths[key]
                value = key
        return value
     def driveToCube(self, cube):
         angle = cubes[cube].rot_x
         R.rotateBy(angle)
         
         
        
        
        
        
        
        