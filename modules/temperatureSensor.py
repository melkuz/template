import RPi.GPIO as GPIO
import time
from ADCDevice import *
import math


class temperatureSensor:
	
    __adc = ADCDevice()

    def __init__(self):
        if (self.__adc.detectI2C(0x4b)):
            self.__adc = ADS7830()
        elif (self.__adc.detectI2C(0x48)):
            self.__adc = PCF8591()
        else:
            print("No correct I2C address found.")
            exit(-1)


    def getTemp(self):
        value = self.__adc.analogRead(0)
        voltage = 100 / 255.0 * 3.3        # calculate voltage
        Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
        tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
        tempC = tempK -273.15        # calculate temperature (Celsius)
        return tempC

    def __del__(self):
        self.__adc.close()
