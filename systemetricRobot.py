from sr import *

class SystemetricRobot(Robot):
    """A class derived from the base `Robot` class provided by soton"""
    def __init__(self):
        #Make sure the soton class is initiated, so we can connect to motors
        Robot.__init__(self)
        
        #Name the motors, for easy access
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]
       
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
    def set_right(self, value):
        self.rightMotor.target = value
    
    def stop(self):
        """Stop the robot, by setting the speed of both motors to 0"""
        self.right = self.left = 0
        
    def drive(self, speed = 50):
        """Drive the robot forwards or backwards at a certain speed"""
        self.right = self.left = speed
        
    def turn(self, speed):
        """Rotate the robot at a certain speed. Positive is clockwise"""
        self.right = -speed
        self.left = speed