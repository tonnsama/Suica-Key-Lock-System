#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
# from keymodule.sensor import *
from gpiozero import DigitalInputDevice as ReedSwitch

reed_switch = ReedSwitch(27)

# GPIO.setmode(GPIO.BCM)
# reed_sw = 27
# GPIO.setup(reed_sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# def isClosed():
# 	if GPIO.input(reed_sw) == GPIO.HIGH:
# 		return True
# 	else:
# 		return False

def isClosed():
  return reed_switch.value


try:
  while True:

    if isClosed():
      print('CLOSED')
    else:
      print('OPEN')
    # print(reed_switch.value)

    time.sleep(0.05)

except KeyboardInterrupt:
  pass
  # GPIO.cleanup()
