import RPi.GPIO as gpio
from time import sleep

#Defining GPIO pin numbers 
pin1 = 6 # This is GPIO6, hence, 5th pin in inner row from ports
pin2 = 7 # 8th pin in outer row from ports
pin3 = 8 # 9th pin in outer row from ports
pin4 = 9 # 10th pin in inner row from ports

# Setting up basic GPIO settings
gpio.setmode(gpio.BCM)
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

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

def move_to_cell(index):
    global pin1
    global pin2
    global pin3
    global pin4
    reset()
    if (index == 1):
        gpio.output(pin1, 1)
    elif (index == 2):
        gpio.output(pin2, 1)
    elif (index == 3):
        gpio.output(pin1, 1)
        gpio.output(pin2, 1)
    elif (index == 4):
        gpio.output(pin3, 1)
    elif (index == 5):
        gpio.output(pin1, 1)
        gpio.output(pin3, 1)
    elif (index == 6):
        gpio.output(pin2, 1)
        gpio.output(pin3, 1)
    elif (index == 7):
        gpio.output(pin1, 1)
        gpio.output(pin2, 1)
        gpio.output(pin3, 1)
    elif (index == 8):
        gpio.output(pin4, 1)
    elif (index == 9):
        gpio.output(pin1, 1)
        gpio.output(pin4, 1)
        
def camera_servo_movement(position):
    global pin1
    global pin2
    global pin3
    global pin4
    reset()
    if (position == 0):
        gpio.output(pin2, 1)
        gpio.output(pin4, 1)
    elif (position == 90):
        gpio.output(pin1, 1)
        gpio.output(pin2, 1)
        gpio.output(pin4, 1)
    elif (position == 180):
        gpio.output(pin3, 1)
        gpio.output(pin4, 1)
        
def reset():
    global pin1
    global pin2
    global pin3
    global pin4
    gpio.output(pin1, 0)
    gpio.output(pin2, 0)
    gpio.output(pin3, 0)
    gpio.output(pin4, 0)
    

# Putting under try block as need to clean up pins on keyboard interrupt
try:
    # Turned off by default
    reset()
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
