from sr import *
from pyeuclid import *

class SystemetricRobot(Robot):
    """A class derived from the base 'Robot' class provided by soton"""     
    def __init__(self):
        #Make sure the soton class is initiated, so we can connect to motors
        Robot.__init__(self)
        
        #Name the motors, for easy access
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]
        
        #Camera orientation
        self.cameraMatrix = Matrix4.new_rotate_euler(
            heading = 0,
            attitude = -10,
            bank = 0
        )
    
    #Getters and setters for left motor. Allows you to write R.left = 100 for full speed forward
    @property
    def left(self):
        """Property to control the speed of the left motor, without the hassle of `.target`"""
        return self.leftMotor.target
        
    @left.setter
    def left(self, value):
        self.leftMotor.target = value
        
    @property  
    def right(self):
        """Property to control the speed of the right motor, without the hassle of `.target`"""
        return self.rightMotor.target
        
    @right.setter    
    def right(self, value):
        self.rightMotor.target = value
    
    def stop(self):
        """Stop the robot, by setting the speed of both motors to 0"""
        self.right = 0
        self.left = 0
        
    def drive(self, speed=50, steer=0):
        """Drive the robot forwards or backwards at a certain speed, with an optional steer"""
        self.right = speed - steer
        self.left = speed + steer
        
    def turn(self, speed):
        """Rotate the robot at a certain speed. Positive is clockwise"""
        self.right = -speed
        self.left = speed
    
    @property 
    def compassHeading(self):
        """Get the compass heading from the mbed"""
        pass
    
    def visibleCubes(self):
        markers = self.see()
        cubes = []
        
        for marker in markers:
            if marker.info.marker_type == MARKER_TOKEN:
                newmarker = {}
                newmarker.seenAt = marker.timestamp
                newmarker.id = marker.info.offset
                newmarker.vertices = []
                
                for v in marker.vertices:
                    newmarker.vertices.append(Point3(
                        v.world.x,
                        v.world.y,
                        v.world.z
                    ))
                
                edge1 = newmarker.vertices[0] - newmarker.vertices[1]
                edge2 = newmarker.vertices[2] - newmarker.vertices[1]
                newmarker.normal = edge1.cross(edge2).normalize()
                
                location = marker.center.world
                newmarker.location = Point3(location.x, location.y, location.z)
                
                cubes.append(newmarker)
        
        return cubes