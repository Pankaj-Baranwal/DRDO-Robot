import RPi.GPIO as gpio
import os
import picamera
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
    
def click_picture():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 15
    camera.capture('image.jpg')
    camera.start_preview()
    camera.vflip = False
    camera.hflip = False
    camera.brightness = 50
    camera.start_preview()
    camera.capture('image.jpg')
    camera.stop_preview()
    print ("Clicked Image")

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
        os.popen("nc -l 2999 > received.txt")
        print ("Received data")
        f = open("received.txt")
        next = (f.readline()).strip()
        if (next == '01'):
            move_to_cell(1)
        elif (next == '02'):
            move_to_cell(2)
        elif (next == '03'):
            move_to_cell(3)
        elif (next == '04'):
            move_to_cell(4)
        elif (next == '05'):
            move_to_cell(5)
        elif (next == '06'):
            move_to_cell(6)
        elif (next == '07'):
            move_to_cell(7)
        elif (next == '08'):
            move_to_cell(8)
        elif (next == '09'):
            move_to_cell(9)
        elif (next == '10'):
            reset()
        elif (next == '11'):
            camera_servo_movement(0)
        elif (next == '12'):
            camera_servo_movement(90)
        elif (next == '13'):
            camera_servo_movement(180)
        elif (next == '00'):
            click_picture()
        os.popen("cat image.jpg | nc 192.168.1.108 | 2999")
        print ("Image sent")
        with open("send.txt", "a") as f
            f.write("1\n")
        os.popen("cat send.txt | nc 192.168.1.108 | 2999")
        print ("number sent")
#         switch_on()
#         print "ON"
#         switch_off()
#         print "OFF"

except KeyboardInterrupt:
    gpio.cleanup()
finally:
    gpio.cleanup()
