import RPi.GPIO as gpio
from time import sleep

#Defining GPIO pin numbers 
pin1 = 7 # This is GPIO7, hence, 8th pin in outer row from ports
pin2 = 8 # 9th pin in outer row from ports
pin3 = 9 # 10th pin in inner row from ports

# Setting up basic GPIO settings
gpio.setmode(gpio.BCM)
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)

# Control LED connected on pin1 as positive and pin2 as negative
def switch_on():
    global pin1
    global pin2
    gpio.output(pin1, 1)
    gpio.output(pin2, 0)
    # Sleep for 2 seconds
    sleep(2)

# Turn off LED
def switch_off():
    global pin1
    global pin2
    gpio.output(pin1, 0)
    gpio.output(pin2, 0)
    sleep(2)

# Putting under try block as need to clean up pins on keyboard interrupt
try:
    # Turned off by default
    gpio.output(pin1, 0)
    gpio.output(pin2, 0)
    # Infinity Loop
    while (1):
        switch_on()
        print "ON"
        switch_off()
        print "OFF"
except KeyboardInterrupt:
    gpio.cleanup()
finally:
    gpio.cleanup()
