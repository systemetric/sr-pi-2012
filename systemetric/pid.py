import threading
import time
import math

class PID(threading.Thread):
    def __init__(self, getInput, setOutput, outputRange = (float("inf"), float("-inf"))):
        threading.Thread.__init__(self)
        
        self.getInput = getInput
        self.setOutput = setOutput

        self.maxOutput, self.minOutput = outputRange
        
        self._target = 0
        self._enabled = False
        
        self._lock = threading.Lock()
        
        self.kp = 0.75
        self.ki = 0
        self.kd = 0
        
        self.period = 0.075
        self._reset()

    @property
    def enabled(self):
        return self._enabled
        
    @enabled.setter
    def enabled(self, value):
        with self._lock:
            if not value:
                self._reset()
                
            self._enabled = value
            
    @property
    def target(self):
        return self._target
        
    @target.setter
    def target(self, value):
        with self._lock:
            self._target = value
            self._reset()
        
    def _reset(self):
        self._lastError = None
        self._totalError = 0
        self._error = float('nan')
    
    def run(self):
        while True:
            with self._lock:
                if self.enabled:
                    self._error = float(self.target - self.getInput())
                    
                    p = self.kp * self._error
                    i = self.ki * self._totalError
                    d = self.kd * (self._error - self._lastError) / period if self._lastError is not None else 0
                    
                    self._lastError = self._error

                    totalError = self._totalError + self._error * period
                        
                    if self.minOutput < totalError * self.ki < self.maxOutput:
                        self._totalError = totalError
                
                    self.setOutput(p + i + d)
                    
            time.sleep(period)
        
    def onTarget(self, tolerance = 5):
        print "error is %.2f" % self._error
        return not self.enabled or math.fabs(self._error) < tolerance
    
    def tuneFromZieglerNichols(ku, pu):
        self.kp = 0.6 * ku
        self.ki = 2 * self.kp / pu
        self.kd = self.kp * pu / 8