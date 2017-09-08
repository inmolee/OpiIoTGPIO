from periphery import GPIO
import time
import signal
import sys

flag = True

def handler(signal, frame):
  global flag
  print('handler')
  flag = False


signal.signal(signal.SIGINT, handler)
# Open GPIO 125 with input direction
gpio_in = GPIO(125, "in")

# Open GPIO 126 with output direction
gpio_out = GPIO(126, "out")

while flag:
  value = gpio_in.read()
  print value
  gpio_out.write(value)
  time.sleep(1.0)


gpio_out.write(False)
gpio_in.close()
gpio_out.close()
