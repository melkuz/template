from ast import Global
from glob import glob
import RPi.GPIO as GPIO
import time



class waterMeasurer:
    __pinT=0
    __pinE=0
    def __init__(self,TRIG,ECHO):
        self.__pinT = TRIG
        self.__pinE = ECHO
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, False)

    def getWaterLevel(self):
        GPIO.output(self.__pinT,True)
        time.sleep(0.00001)
        GPIO.output(self.__pinT,False)

        while GPIO.input(self.__pinE)== 0:
            pulse_start = time.time()
        
        while GPIO.input(self.__pinE)==1:
            pulse_stop = time.time()

        pulse_time = pulse_stop - pulse_start
        waterLevel = pulse_time * 17150
        print(round(waterLevel, 2));
        time.sleep(1)
        return waterLevel
