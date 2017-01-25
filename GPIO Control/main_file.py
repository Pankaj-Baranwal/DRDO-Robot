import RPi.GPIO as gpio
from time import sleep

#Defining GPIO pin numbers 
pin1 = 7
pin2 = 8

#Setting up basic GPIO settings
gpio.setmode(gpio.BCM)
