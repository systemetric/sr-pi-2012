from systemetric.compassrobot import *
import time

def main():
    regulator = CompassRobot().regulator

    regulator.kp = 2
    regulator.ki = 0
    regulator.kd = 0
    regulator.target = 0
    regulator.enabled = True

    while True:
        pass
