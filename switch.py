import time

from gpiozero import DigitalInputDevice as ReedSwitch


rs_1 = ReedSwitch(19)
rs_2 = ReedSwitch(26)

while True:
	print("rs_1: {}, rs_2: {}".format(rs_1.value, rs_2.value))
	time.sleep(0.1)
