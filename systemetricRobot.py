from sr import *

class SystemetricRobot(Robot):
    def __init__(self):
        Robot.__init__(self)
        print("Actually Running")
        
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]
        print("Found motors")
        print(self.motors)
        
    def get_left(self):
        return self.leftMotor.target
            
    def set_left(self, value):
        self.leftMotor.target = value
        
    left = property(get_left, set_left)
        
        
    def get_right(self):
        return self.rightMotor.target
            
    def set_right(self, value):
        self.rightMotor.target = value
        
    right = property(get_right, set_right)