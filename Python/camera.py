import picamera
from time import sleep
from PIL import Image
import socket

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.capture('image.jpg')
camera.start_preview()
camera.vflip = False
camera.hflip = False
camera.brightness = 50
camera.start_preview()
for i in range(10):
    sleep(0.5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    camera.stop_preview()
    print ("hey")
