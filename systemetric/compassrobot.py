#Critical p value 2.575
#Oscilations per minute = 86
#Oscilation period = 0.698s

import time
import threading
import math
from twowheeledrobot import TwoWheeledRobot
from compass import Compass
from pid import PID

class CompassRobot(TwoWheeledRobot):

    def __init__(self):
        TwoWheeledRobot.__init__(self)
        self.compass = Compass()

        self.regulator = PID(
            getInput = lambda: self.compass.heading,
            setOutput = lambda x: self.drive(speed = self.speed, steer = x),
            outputRange = (-100, 100),
            iLimit = 0.25
        )
        #self.regulator.tuneFromZieglerNichols(2.575, 0.698)

        #PID settings
        self.regulator.kp = 0.725
        self.regulator.ki = 2 #Needs more testing
        self.regulator.kd = 0.0325

        self.regulator.start()

        self.speed = 0
        
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
        
        while not self.regulator.onTarget(tolerance = 2.5):
            time.sleep(0.05)
        
    def rotateBy(self, angle, fromTarget = False):
        self.regulate = True
        self.speed = 0
        self.rotateTo((self.regulator.target if fromTarget else self.compass.heading) + angle)
        
    def setSpeed(self, speed):
        self.regulate = True
        self.speed = speed
        
    def stop(self):
        self.speed = 0
        self.regulate = False
        TwoWheeledRobot.stop(self)