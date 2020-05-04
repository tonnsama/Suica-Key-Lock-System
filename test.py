from keymodule.sensorNew import *
import time

while True:
    if isClosed():
      print('CLOSED')
    else:
      print('OPEN')
    # print(reed_switch.value)

    time.sleep(0.05)
