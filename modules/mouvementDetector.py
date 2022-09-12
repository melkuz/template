import RPi.GPIO as GPIO
import time

class mouvementDetector:
    __pinSensor = 0
    
    def __init__(self,pinSensor):
        GPIO.setup(pinSensor,GPIO.IN)
        self.__pinSensor = pinSensor

    def detecMove(self):
        return GPIO.input(self.__pinSensor)
