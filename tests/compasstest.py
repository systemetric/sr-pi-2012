import time
import threading

from systemetricRobot import SystemetricRobot

class compassThread(threading.Thread):
    def __init__(self, R):
        self.R = R
        self.target = 0
        self.speed = 0
        self.running = True
        
    def run(self):
        while self.running:
            heading = self.R.compassHeading
            error = self.target - heading 
            while error >= 180:
                error -= 360
            while error < -180:
                error += 360
            
            self.R.drive(speed = self.speed, steer = error/2)

def main():
    R = SystemetricRobot()
    t = compassThread(R)
    t.start()