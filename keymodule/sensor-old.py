import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
reed_sw = 27
GPIO.setup(reed_sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def isClosed():
	if GPIO.input(read_sw) == GPIO.HIGH:
		return True
	else:
		return False
