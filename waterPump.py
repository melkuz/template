
from ast import Global
from glob import glob
import RPi.GPIO as GPIO
import time
import math

from modules.led import led
from modules.mouvementDetector import mouvementDetector
from modules.pompeMotor import pompeMotor
from modules.switch import switch
from modules.temperatureSensor import temperatureSensor
from modules.waterMeasurer import waterMeasurer

GPIO.setwarnings(False)


#PINS#

motorPin1 = 27
motorPin2 = 17
enablePin = 22
TRIG = 5
ECHO = 6
switchPin = 24
currentstate = "E1"
sensorMouvementPin = 26
rDel = 25


# le polus grand veut dire moins d'eau car c'est le temps calcule entre l'eau et le detecteur de niveau deau
maxWaterLevel = 15
minWaterLevel = 19


#initialisation de chaque objet par madule RPGIO
switch = switch(switchPin)
mouvementDetector = mouvementDetector(sensorMouvementPin)
led = led(rDel)
pompeMotor = pompeMotor(motorPin1,motorPin2,enablePin)
temperatureSensor = temperatureSensor()
waterMeasurer = waterMeasurer(TRIG,ECHO)



def setup():
    GPIO.add_event_detect(switchPin, GPIO.FALLING)
    pompeMotor.setPower(0)
   

def E1():
    global switch
    global mouvementDetector
    global led
    global pompeMotor
    global temperatureSensor
    global waterMeasurer
    global currentstate
    
    led.ledO()
    if(GPIO.event_detected(switchPin)):
    	switch.changeState()
    if switch.getState() and temperatureSensor.getTemp() > 0: ## verifie que la temperature est plus grande que 0
        currentstate = "E2"
    

def E2():
    global switch
    global mouvementDetector
    global led
    global pompeMotor
    global temperatureSensor
    global waterMeasurer
   
   
    global currentstate
    
    led.ledOn()

    if switch.getState():
        pompeMotor.setPower(0)
        currentstate = "E1"
        return

    waterLevel = waterMeasurer.getWaterLevel()

    if mouvementDetector.detecMove() and temperatureSensor.getTemp() > 0:
        if waterLevel > maxWaterLevel:
            led.ledOff()
            currentstate = "E3"
        else:
            print("la fontaine d'eau est pleine")
            
#function qui cherche l niveau d'eau dependement de ce qui a ete mis dans le serveur mqtt     

    
def E3(): 
    global switch
    global mouvementDetector
    global led
    global pompeMotor
    global temperatureSensor
    global waterMeasurer
    global currentstate
    
    
    waterLevel = waterMeasurer.getWaterLevel()
 

    if waterLevel < maxWaterLevel:
        print("Water full")
        currentstate = "E2"
        pompeMotor.setPower(0)
        
        return
    else:
        pompeMotor.setPower(100)

    if switch.getState() and temperatureSensor.getTemp() > 0:
        pompeMotor.setPower(0)
        currentstate = "E1"
        return

def loop():
    global currentstate
    currentstate = "E2"
    print(currentstate)
    while (True):
        if currentstate == "E1":
            E1()
            print(currentstate)
        elif currentstate == "E2":
            E2() 
            print(currentstate)
            # Validation des conditions pour la mise à jour de l'état

        elif currentstate == "E3":
            print(currentstate)
            E3()
            
            # Validation des conditions pour la mise à jour de l'état


def destroy():
    
    GPIO.cleanup()


if __name__ == '__main__': # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()