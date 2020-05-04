from gpiozero import AngularServo, RGBLED
from colorzero import Color
from time import sleep

servo = AngularServo(17, min_angle=-45, max_angle=45)
red, green, blue = 3, 4, 2
led = RGBLED(red, green, blue, False)

move_time = 1.5

def lock():
  servo.min()
  sleep(move_time)
  servo.detach()
  led.color = Color('red')

def unlock():
  servo.max()
  sleep(move_time)
  servo.detach()
  led.color = Color('blue')

def wrongCard(key_state):
  for i in range(3):
    led.color = Color('red')
    sleep(0.1)
    led.off()
    sleep(0.1)

  if key_state:
    print('Current state is Locked')
    led.color = Color('red')
  else:
    print('Current state is Unlocked')
    led.color = Color('blue')


# if __name__ == '__main__':
#   unlock()
#   sleep(2)
#   lock()
#   sleep(2)
#   wrongCard(True)
#   while True:
#     led.color = Color('red')
#     sleep(1)
#     led.color = Color('blue')
#     sleep(1)
