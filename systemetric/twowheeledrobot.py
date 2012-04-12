from sr import *
import math
import atexit

def _motorSpeedTransform(signedSpeed):
    speed = abs(signedSpeed)
    #From excel:
    #          normalized = 36.351ln(power) - 47.136
    # normalized + 47.136 = 36.351ln(power)
    # (normalized + 47.136) / 36.351 = ln(power)
    power = math.exp((speed + 47.136) / 36.351)
    if power <= 4:
        power = 0
    power = max(0, min(100, power))
    return int(math.copysign(power, signedSpeed))

class TwoWheeledRobot(Robot):
    def __init__(self):
        #Make sure the soton class is initiated, so we can connect to motors
        Robot.__init__(self)
        atexit.register(self.stop)
        
        #Name the motors, for easy access
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]

        self._leftSpeed = 0
        self._rightSpeed = 0
        
    #Getters and setters for left motor. Allows you to write R.left = 100 for full speed forward
    @property
    def left(self):
        '''Property to control the speed of the left motor, without the hassle of `.target`'''
        return self._leftSpeed
        
    @left.setter
    def left(self, value):
        if not math.isnan(value):
            self._leftSpeed = value
            self.leftMotor.target = _motorSpeedTransform(value)
        
    @property  
    def right(self):
        '''Property to control the speed of the right motor, without the hassle of `.target`'''
        return self._rightSpeed
        
    @right.setter
    def right(self, value):
        if not math.isnan(value):
            self._rightSpeed = value
            self.rightMotor.target = _motorSpeedTransform(value)
    
    def stop(self):
        '''Stop the robot, by setting the speed of both motors to 0'''
        self.right = 0
        self.left = 0

    def drive(self, speed=50, steer=0):
        '''Drive the robot forwards or backwards at a certain speed, with an optional steer'''
        self.left = speed - steer
        self.right = speed + steer
        
    def turn(self, speed):
        '''Rotate the robot at a certain speed. Positive is clockwise'''
        self.right = speed
        self.left = -speed
