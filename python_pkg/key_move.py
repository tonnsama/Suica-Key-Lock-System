import RPi.GPIO as GPIO
import os, time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

servoChannel = 0
Lock_pos = 100
Unlock_pos = 200

ledR = 3 #LED color RED
ledB = 2 #LED color BLUE

GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)

def servo(position):
	s = 'echo {0}={1} > /dev/servoblaster'.format(servoChannel, position)
	os.system(s)

def lock():
	servo(Lock_pos)
	time.sleep(1.5)
	GPIO.output(ledR, False)
	GPIO.output(ledB, True)
	servo(0)

def unlock():
	servo(Unlock_pos)
	time.sleep(1.5)
	GPIO.output(ledR, True)
	GPIO.output(ledB, False)
	servo(0)

def wrongCard(key_state):
	GPIO.output(ledB, True)
	for i in range(3):
		GPIO.output(ledR, True)
		time.sleep(0.1)
		GPIO.output(ledR, False)
		time.sleep(0.1)

	if key_state: # current state is Locked
		print("Current state is Locked")
		GPIO.output(ledB, True)
		GPIO.output(ledR, False)
	else:	      # current state is Unlocked
		print("Current state is Unlocked")
		GPIO.output(ledR, True)
		GPIO.output(ledB, False)
