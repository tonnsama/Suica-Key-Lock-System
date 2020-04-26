import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
read_sw = 27
GPIO.setup(read_sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def is_closed():
	if GPIO.input(read_sw) == GPIO.HIGH:
		return True
	else:
		return False
