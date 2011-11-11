from sr import *

class TwoWheeledRobot(Robot):
    def __init__(self):
        #Make sure the soton class is initiated, so we can connect to motors
        Robot.__init__(self)
        
        #Name the motors, for easy access
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]
        
    #Getters and setters for left motor. Allows you to write R.left = 100 for full speed forward
    @property
    def left(self):
        '''Property to control the speed of the left motor, without the hassle of `.target`'''
        return self.leftMotor.target
        
    @left.setter
    def left(self, value):
        if not math.isnan(value):
            self.leftMotor.target = value
        
    @property  
    def right(self):
        '''Property to control the speed of the right motor, without the hassle of `.target`'''
        return self.rightMotor.target
        
    @right.setter    
    def right(self, value):
        if not math.isnan(value):
            self.rightMotor.target = value
    
    def stop(self):
        '''Stop the robot, by setting the speed of both motors to 0'''
        self.right = 0
        self.left = 0
        
    def drive(self, speed=50, steer=0):
        '''Drive the robot forwards or backwards at a certain speed, with an optional steer'''
        self.right = speed - steer
        self.left = speed + steer
        
    def turn(self, speed):
        '''Rotate the robot at a certain speed. Positive is clockwise'''
        self.right = -speed
        self.left = speed
    