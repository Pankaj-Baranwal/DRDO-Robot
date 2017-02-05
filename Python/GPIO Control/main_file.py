import RPi.GPIO as gpio
import os
import picamera
from time import sleep

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.vflip = False
camera.hflip = False
camera.brightness = 50
counter = 0

#Defining GPIO pin numbers 
pin1 = 6 # This is GPIO6, hence, 5th pin in inner row from ports
pin2 = 7 # 8th pin in outer row from ports
pin3 = 8 # 9th pin in outer row from ports
pin4 = 9 # 10th pin in inner row from ports

# Setting up basic GPIO settings
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
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
    global camera
    global counter
    camera.start_preview()
    sleep(0.5)
    if (counter == 3):
        counter = 0
    camera.capture('image%s.jpg'%counter)
    counter = counter + 1
    camera.stop_preview()
    print ("Clicked Image")
    sleep(2)
    os.popen("cat image.jpg | nc 192.168.1.108 2999")
    print ("Image sent")
    with open("send.txt", "w") as f:
        f.write("1\n")
    os.popen("cat send.txt | nc 192.168.1.108 2999")
    print ("number sent")

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
    camera_servo_movement(0)
    camera_servo_movement(90)
    camera_servo_movement(180)
        
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
    click_picture()
        
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
    camera_servo_movement(0)
    camera_servo_movement(90)
    camera_servo_movement(180)
    while (1):
        os.popen("nc -l 2999 > received.txt")
        print ("Received data")
        f = open("received.txt")
        next = (f.readline()).strip()
        print (next)
        if (next == '1'):
            move_to_cell(1)
        elif (next == '2'):
            move_to_cell(2)
        elif (next == '3'):
            move_to_cell(3)
        elif (next == '4'):
            move_to_cell(4)
        elif (next == '5'):
            move_to_cell(5)
        elif (next == '6'):
            move_to_cell(6)
        elif (next == '7'):
            move_to_cell(7)
        elif (next == '8'):
            move_to_cell(8)
        elif (next == '9'):
            move_to_cell(9)
        elif (next == '10'):
            reset()
        elif (next == '11'):
            camera_servo_movement(0)
        elif (next == '12'):
            camera_servo_movement(90)
        elif (next == '13'):
            camera_servo_movement(180)
        elif (next == '0'):
            camera_servo_movement(0)
            camera_servo_movement(90)
            camera_servo_movement(180)
#         switch_on()
#         print "ON"
#         switch_off()
#         print "OFF"

except KeyboardInterrupt:
    gpio.cleanup()
finally:
    gpio.cleanup()
