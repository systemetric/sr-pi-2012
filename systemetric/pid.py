import threading
import time
import math

class PID(threading.Thread):
    def __init__(self, getInput, setOutput, outputRange = (float("-inf"), float("inf")), iLimit = 1):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.getInput = getInput
        self.setOutput = setOutput

        self.minOutput, self.maxOutput = outputRange
        self.iLimit = iLimit
        
        self._target = 0
        self._enabled = False
        
        self._lock = threading.Lock()
        
        self.kp = 0.25
        self.ki = 0
        self.kd = 0
        
        self.period = 0.025
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
        self.error = float('nan')
    
    def run(self):
        while True:
            with self._lock:
                if self.enabled:
                    self.error = float(self.target - self.getInput())
                    
                    p = self.kp * self.error
                    i = self.ki * self._totalError
                    d = self.kd * (self.error - self._lastError) / self.period if self._lastError is not None else 0
                   
                   # print time.time(), self.error, p, self.kp, d, self.kd

                    self._lastError = self.error

                    totalError = self._totalError + self.error * self.period
                        
                    if self.iLimit*self.minOutput < totalError * self.ki < self.iLimit*self.maxOutput:
                        self._totalError = totalError
                
                    self.setOutput(p + i + d)
                    
            time.sleep(self.period)
        
    def onTarget(self, tolerance = 5):
        return not self.enabled or abs(self.error) < tolerance
    
    def tuneFromZieglerNichols(self, ku, pu):
        self.kp = 0.6 * ku
        self.ki = 2 * self.kp / pu
        self.kd = self.kp * pu / 8