import RPi.GPIO as GPIO
import time


class pompeMotor:
    __motorPin1 = 0
    __motorPin2 = 0
    __pmw = None
    __power = 0

    def setPmw(self):
        print("pwm level : " + str(self.__power))
        self.__pmw.start(self.__power)
        GPIO.output(self.__motorPin1,GPIO.HIGH) # motorPin1 output HIHG level
        GPIO.output(self.__motorPin2,GPIO.LOW) # motorPin2 output LOW level
        
    def __init__(self,motorPin1,motorPin2,enablePin):
        self.__motorPin1 = motorPin1
        self.__motorPin2 = motorPin2
        GPIO.setup(motorPin1,GPIO.OUT) # set pins to OUTPUT mode
        GPIO.setup(motorPin2,GPIO.OUT)
        GPIO.setup(enablePin,GPIO.OUT)
        self.__pmw = GPIO.PWM(enablePin,1000) # creat PWM and set Frequence to 1KHz
        

    def setPower(self, p):
        self.__power =p
        self.setPmw()

    
    def __del__(self):
        self.__pmw.stop()

