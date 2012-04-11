#Critical p value 2.575
#Oscilations per minute = 86
#Oscilation period = 0.698s

import time
from twowheeledrobot import TwoWheeledRobot
from compass import Compass
from pid import PID

class CompassRobot(TwoWheeledRobot):
    def __init__(self):
        TwoWheeledRobot.__init__(self)
        self.compass = Compass()

        self.regulator = PID(
            getInput = lambda: self.compass.heading,
            setOutput = lambda x: TwoWheeledRobot.drive(self, speed = self.speed, steer = x),
            outputRange = (-100, 100),
            iLimit = 0.25
        )
        #self.regulator.tuneFromZieglerNichols(2.575, 0.698)

        #PID settings
        self.regulator.kp = 1.500 # FIRST this number started at 0 and was raised until it started to oscillate
        self.regulator.ki = 0.175 # THIRD we changed until it stopped dead on.
        self.regulator.kd = 0.080 # SECOND we changed kd until the amount it overshot by was reduced

        self.regulator.start()

        self.speed = 0
        
    @property
    def regulate(self):
        """Shorthand for enabling and disabling the PID controller"""
        return self.regulator.enabled
        
    @regulate.setter
    def regulate(self, value):
        self.regulator.enabled = value
         
    def rotateTo(self, heading, tolerance = 2.5):
        """
        Rotate the robot to face the specified heading. Return when within
        tolerance degrees of the target. Note that this does not stop the motors
        upon returning
        """
        self.regulate = True;
        self.speed = 0
        self.regulator.target = heading
        
        while not self.regulator.onTarget(tolerance=tolerance):
            time.sleep(0.05)
        
    def rotateBy(self, angle, fromTarget = False):
        """
        Rotate the robot a certain angle from the direction it is currently
        facing. Optionally rotate from the last target, preventing errors
        accumulating
        """
        self.regulate = True
        self.speed = 0
        self.rotateTo((self.regulator.target if fromTarget else self.compass.heading) + angle)
        
    def setSpeed(self, speed):
        print "deprecated - use drive instead"
        self.drive(speed, regulate = True)

    def drive(self, speed, steer = 0, regulate = True):
        """
        Drive the robot at a certain speed, by default using the compass to
        regulate the robot's heading.

        TODO: Tune PID controller for straight movement.
        """
        self.regulate = regulate
        if regulate:
            self.speed = speed
        else:
            TwoWheeledRobot.drive(self, speed, steer)
            
        
    def stop(self):
        """
        Stop the robot, by setting the speed to 0, and disabling regulation
        """
        self.speed = 0
        self.regulate = False
        TwoWheeledRobot.stop(self)