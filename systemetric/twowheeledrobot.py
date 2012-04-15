from sr import Robot
import math
import atexit
import threading
import logs

def _motorSpeedTransform(signedSpeed):
    speed = abs(signedSpeed)
    if speed == 100:
        return signedSpeed
    #From excel:
    #          normalized = 36.351ln(power) - 47.136
    # normalized + 47.136 = 36.351ln(power)
    # (normalized + 47.136) / 36.351 = ln(power)
    power = math.exp((speed + 47.136) / 36.351)
    if power <= 4:
        power = 0
    power = max(0, min(100, power))
    return int(math.copysign(power, signedSpeed))

class AccessRevoked(Exception):
    """Thrown when a thread attempts to control the robot after its access has been revoked"""
    pass

class SingleThreadAccess(object):
    """
    Allow only one thread access to the resource at a time. At any time a
    thread can grab control, causing attribute access in other threads to throw
    an exception, revoking control from the others. Base class members can
    still be accessed through super.
    """
    def __init__(self):
        self.owners = [threading.current_thread()]

    def __getattribute__(self, attr):
        if attr not in ('owners', 'takeControl', 'hasControl') and not self.hasControl:
            raise AccessRevoked
        return super(SingleThreadAccess, self).__getattribute__(attr)

    def takeControl(self, kick=True):
        """Take control of the object, revoking access to all other threads"""
        if kick:
            self.owners = [threading.current_thread()]
        else:
            self.owners.append(threading.current_thread())

    @property
    def hasControl(self):
        """
        Check if the current thread has control - not required in user code.
        Daemon threads, such as the PID, always have access
        """
        return threading.current_thread() in self.owners or threading.current_thread().daemon

class TwoWheeledRobot(Robot, SingleThreadAccess):
    def __init__(self):
        SingleThreadAccess.__init__(self)
        #Make sure the soton class is initiated, so we can connect to motors
        Robot.__init__(self, wait_start = False)
        atexit.register(self.stop)
        
        #Name the motors, for easy access
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]

        self._leftSpeed = 0
        self._rightSpeed = 0
        
    def takeControl(self, *args, **kargs):
        super(TwoWheeledRobot, self).takeControl(*args, **kargs)
        self.stop()
        
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

    def waitForStart(self):
        self._wait_start()
        logs.roundStarted()
