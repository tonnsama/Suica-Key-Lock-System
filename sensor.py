import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

Trig = 24
Echo = 23

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
GPIO.output(Trig, GPIO.LOW)

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
