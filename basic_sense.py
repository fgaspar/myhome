import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
state = True
while (True):
    GPIO.output(16, state)
    state = not state
    time.sleep(5)