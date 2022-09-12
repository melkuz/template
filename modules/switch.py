import RPi.GPIO as GPIO


class switch:
    __status = False

    def __init__(self, pinSwitch):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinSwitch, GPIO.IN, GPIO.PUD_UP)
        print ("switch")

    def changeState(self):
        if self.__status == False:
            self.__status == True
        else:
            self.__status == False

    def getState(self):
        return self.__status
        
