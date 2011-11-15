import systemetric
class RobotCube(object):
    def __init__(self):
        self.R = systemetric.Robot()
    
    def check(self):
        if self.R.getMarkersById().tokens:
            return 1
        else:
            return 0
            
    def shortestDistance(self)
        self.cubes = self.R.getMarkersById().tokens
        self.lengths = {}
        
        #Are there really going to be markers closer than 0?
        distance = 0
        nearest = None
        
        for tokenId, markers in cubes:
            self.lengths[tokenId] = markers[0].dist
            
            #Won't this find the furthest one?
            if self.lengths[tokenId] > distance:
                distance = self.lengths[tokenId]
                nearest = tokenId
                
        return nearest
        
     def driveToCube(self, cube, iterate=10):
         for i in range(iterate):
             R.setSpeed(cubes[cube].dist/2)
             wait(0.1)
             R.setSpeed(0)
             wait(0.1)
             cube = self.shortestDistance()
             angle = cubes[cube].rot_x
             R.rotateBy(angle)