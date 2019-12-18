import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # set board mode to Broadcom


red = 24
yellow = 4
green = 3
blue = 2
white = 17

test = green

GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(white, GPIO.OUT)

GPIO.output(red, 0)
GPIO.output(yellow, 0)
GPIO.output(green, 0)
GPIO.output(blue, 0)
GPIO.output(white, 0)

while True:
   GPIO.output(test, 1)  # turn on pin 5
   time.sleep(1)      # wait 1 second
   GPIO.output(test, 0)  # turn off pin 5
   time.sleep(1)      # wait 1 second
