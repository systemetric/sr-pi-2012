import threading
import time
import math

class PID(threading.Thread):
    D_SAMPLES = 5
    def __init__(self, getInput, setOutput, outputRange = (float("inf"), float("-inf"))):
        threading.Thread.__init__(self)
        
        self.getInput = getInput
        self.setOutput = setOutput

        self.maxOutput, self.minOutput = outputRange
        
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
        self._lastErrors = []
        self._totalError = 0
        self._error = float('nan')
    
    def run(self):
        while True:
            with self._lock:
                if self.enabled:
                    self._error = float(self.target - self.getInput())
                    
                    p = self.kp * self._error
                    i = self.ki * self._totalError
                    d = self.kd * self.__gradient() * self.period
                    
                    self._lastErrors += [self._error]

                    totalError = self._totalError + self._error * self.period
                        
                    if self.minOutput < totalError * self.ki < self.maxOutput:
                        self._totalError = totalError
                
                    self.setOutput(p + i + d)
                    
            time.sleep(self.period)

    def __gradient(self):
        '''calculate the gradient of a bunch of points'''
        while len(self._lastErrors) > 5:
            self._lastErrors = self._lastErrors[:-1]

        #self._lastErrors = self._lastErrors[:-5] if len(self._lastErrors) > 10 else self._lastErrors
        if len(self._lastErrors) <= 5 and len(self._lastErrors) > 1:
            sum_i = 0
            sum_error = 0
            sum_i_squared = 0
            sum_iError = 0

            for i, error in enumerate(self._lastErrors):
                sum_i += i
                sum_error += error
                sum_i_squared += i*i
                sum_iError += i*error
            return (sum_iError - sum_i*sum_error) / (sum_i_squared - sum_i**2)

        else:
            print 'just returned zero for the gradient'
            return 0
        
    def onTarget(self, tolerance = 5):
        return not self.enabled or math.fabs(self._error) < tolerance
    
    def tuneFromZieglerNichols(self, ku, pu):
        self.kp = 0.6 * ku
        self.ki = 2 * self.kp / pu
        self.kd = self.kp * pu / 8