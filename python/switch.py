#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

sw_pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
  while True:
    if GPIO.input(sw_pin) == GPIO.HIGH:
      print('Switch ON')
    else:
      print('Switch OFF')
    time.sleep(0.05)

except KeyboardInterrupt:
  pass
  GPIO.cleanup()
