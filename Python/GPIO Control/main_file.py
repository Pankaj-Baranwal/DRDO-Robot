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

prev_time = 0
    
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
    global pin1
    global pin2
    global pin3
    global pin4
    if (index == 1):
        option = 'a'
    elif (index == 2):
        option = 'b'
    elif (index == 3):
        option = 'c'
    elif (index == 4):
        option = 'd'
    elif (index == 5):
        option = 'e'
    elif (index == 6):
        option = 'f'
    elif (index == 7):
        option = 'g'
    elif (index == 8):
        option = 'h'
    elif (index == 9):
        option = 'i'
    write_serial = arduino.write(str(option))

    arduino.read()
    read_serial = arduino.read()
    if (read_serial == 't'):    
        camera_servo_movement(0)
        camera_servo_movement(90)
        camera_servo_movement(180)
    else:
        print ("Something went wrong while processing instruction!")
        
def camera_servo_movement(position):
    if (position == 0):
        option = 'r'
    elif (position == 90):
        option = 'z'        
    elif (position == 180):
        option = 'l'        
    write_serial = arduino.write(str(option))

    arduino.read()
    read_serial = arduino.read()
    if (read_serial == 't'):    
        click_picture()
    else:
        print ("Something went wrong while processing instruction!")
    
current_milli_time = lambda: int(round(time() * 1000))
    
# Putting under try block as need to clean up pins on keyboard interrupt
try:
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
            # reset
        elif (next == '11'):
            camera_servo_movement(0)
        elif (next == '12'):
            camera_servo_movement(90)
        elif (next == '13'):
            camera_servo_movement(180)
        elif (next == '0'):
            #reset
            
except KeyboardInterrupt:
    gpio.cleanup()
    camera.stop_preview()
finally:
    gpio.cleanup()
    camera.stop_preview()
