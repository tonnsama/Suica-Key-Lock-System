from sensor import measure
from time import sleep

while True:
  d = measure()
  print d
  sleep(0.1)
