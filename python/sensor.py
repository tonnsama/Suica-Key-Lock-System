import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

Trig = 24
Echo = 23
read_sw = 27

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
GPIO.output(Trig, GPIO.LOW)
GPIO.setup(read_sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def measure():
	# Triger
	GPIO.output(Trig, True)
	time.sleep(0.00001)
	GPIO.output(Trig, False)

	while GPIO.input(Echo) == 0:
		startTime = time.time()
	while GPIO.input(Echo) == 1:
		stopTime = time.time()

	passedTime = stopTime - startTime
	distance = passedTime * 17000

	return distance

def is_closed():
	if GPIO.input(read_sw) == GPIO.HIGH:
		return True
	else:
		return False
