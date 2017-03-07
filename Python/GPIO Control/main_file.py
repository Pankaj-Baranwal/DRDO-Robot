import RPi.GPIO as gpio
import os
import picamera
from time import sleep, time


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.vflip = True
camera.hflip = True
camera.brightness = 50
counter = 0
camera.start_preview()
sleep(0.5)

#Defining GPIO pin numbers 
pin1 = 6 # This is GPIO6, hence, 5th pin in inner row from ports
pin2 = 7 # 8th pin in outer row from ports
pin3 = 8 # 9th pin in outer row from ports
pin4 = 9 # 10th pin in inner row from ports
prev_time = 0

# Setting up basic GPIO settings
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)
    
def click_picture():
    global camera
    global counter
    if (counter == 3):
        counter = 0
    camera.capture('image%s.jpg'%counter)
    print ("Clicked Image")
    sleep(0.5)
    os.popen("cat image%s.jpg | nc 192.168.1.112 2999"%counter)
    counter = counter + 1
    print ("Image sent")

def move_to_cell(index):
    print ('GOT IN')
    global pin1
    global pin2
    global pin3
    global pin4
    wait_time = 4
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
    sleep(wait_time)
    camera_servo_movement(0)
    camera_servo_movement(90)
    camera_servo_movement(180)
        
def camera_servo_movement(position):
    global pin1
    global pin2
    global pin3
    global pin4
    wait_time = 1.5
    if (position == 0):
        gpio.output(pin2, 1)
        gpio.output(pin4, 1)
	wait_time = 2.5
    elif (position == 90):
        gpio.output(pin1, 1)
        gpio.output(pin2, 1)
        gpio.output(pin4, 1)
    elif (position == 180):
        gpio.output(pin3, 1)
        gpio.output(pin4, 1)
    print (position)
    sleep(wait_time)
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
    sleep(1)
    
current_milli_time = lambda: int(round(time() * 1000))
    

# Putting under try block as need to clean up pins on keyboard interrupt
try:
    # Turned off by default
    reset()
    # Infinity Loop
    camera_servo_movement(0)
    camera_servo_movement(90)
    camera_servo_movement(180)
    prev_time = current_milli_time()
    with open("send.txt", "w") as f:
        f.write("---x---")
    while (1):
        os.popen("nc -l 2999 > received.txt")
        print ("Received data")
        f = open("received.txt")
        next = (f.readline()).strip()
        print (next)
        with open("send.txt", "a") as f:
            f.write("Moved to cell %s  %s\n"%(next, (current_milli_time()-prev_time)))
        prev_time = current_milli_time()
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
    camera.stop_preview()
finally:
    gpio.cleanup()
    camera.stop_preview()
