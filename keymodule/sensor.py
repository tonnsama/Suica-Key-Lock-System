from gpiozero import DigitalInputDevice as ReedSwitch

reed_switch = ReedSwitch(27)

def isClosed():
  return reed_switch.value
