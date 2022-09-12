import RPi.GPIO as GPIO

class led:
    __status = "OFF"
    __ledPin = 0
    def __init__(self, ledPin):
        self.__ledPin = ledPin
        GPIO.setup(ledPin,GPIO.OUT) # set the ledPin to OUTPUT mode
        GPIO.output(ledPin,GPIO.LOW) # make ledPin output LOW level

    def updateLed(self):
        if self.__status == "ON":
            GPIO.output(self.__ledPin,GPIO.HIGH)
        else:
            GPIO.output(self.__ledPin,GPIO.LOW)
     
    def ledOn(self):
        self.__status = "ON"
        print("led on")
        self.updateLed()

    def ledOff(self):
        self.__status = "OFF"
        print("led off")
        self.updateLed()

            