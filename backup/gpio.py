import RPi.GPIO as GPIO
import time

#GPIO.cleanup()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ch = 2

GPIO.setup(ch, GPIO.OUT)

GPIO.output(ch, False)
