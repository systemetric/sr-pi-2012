print 'I\'m on the first line!'
print 'second line!'

import time
import threading
import math
from twowheeledrobot import TwoWheeledRobot
from compass import Compass
from pid import PID

class CompassRobot(TwoWheeledRobot):

    """
    class CompassThread(threading.Thread):
        def __init__(self, robot):
            threading.Thread.__init__(self)
            self.robot = robot
            self.targetHeading = 0
            self.speed = 0
            
            self._enabled = False
            
            self.lock = threading.Lock()
            
            self.p = 0.75
        
        @property
        def enabled(self):
            return self._enabled
            
        @enabled.setter
        def enabled(self, value):
            with self.lock:
                self._enabled = value
            
        def run(self):
            while True:
                with self.lock:
                    if self.enabled:
                        heading = self.robot.compass.heading
                        error = float(self.targetHeading - heading)

                        correctBy = self.p * error
                    
                        self.robot.drive(speed = self.speed, steer = correctBy)
                time.sleep(0.05)
            
        def onTarget(self, tolerance = 5):
            return math.fabs(float(self.targetHeading - self.robot.compass.heading)) < tolerance
"""
    def __init__(self):
        TwoWheeledRobot.__init__(self)
        self.compass = Compass()

        self.regulator = PID(
            getInput = lambda: self.compass.heading,
            setOutput = lambda x:self.drive(speed = self.speed, steer = x)
        )
        #self.regulator.ki = 0.1
        self.regulator.start()
        
    @property
    def regulate(self):
        return self.regulator.enabled
        
    @regulate.setter
    def regulate(self, value):
        self.regulator.enabled = value
         
    def rotateTo(self, heading):
        self.regulate = True;
        self.speed = 0
        self.regulator.target = heading
        
        while not self.regulator.onTarget():
            time.sleep(0.05)
        
    def rotateBy(self, angle):
        self.regulate = True
        self.speed = 0
        self.rotateTo(self.compass.heading + angle)
        
    def setSpeed(self, speed):
        self.regulate = True
        self.speed = speed
        
    def stop(self):
        self.speed = 0
        self.regulate = False
        TwoWheeledRobot.stop(self)