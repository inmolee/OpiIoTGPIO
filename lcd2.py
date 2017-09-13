#!/usr/bin/python
#-*- encoding: utf-8 -*-
#import
from periphery import GPIO
import time
import sys

# Define GPIO to LCD mapping
GPIO.LCD_RS = GPIO(101, "out")
GPIO.LCD_E  = GPIO(121, "out")
GPIO.LCD_D4 = GPIO(122, "out")
GPIO.LCD_D5 = GPIO(123, "out")
GPIO.LCD_D6 = GPIO(124, "out")
GPIO.LCD_D7 = GPIO(125, "out")

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def main(message):
  # Main program block
#  GPIO_setwarnings(False)
#  GPIO_setmode(GPIO_BCM)       # Use BCM GPIO numbers
#  GPIO_setup(LCD_E, GPIO_OUT)  # E
#  GPIO_setup(LCD_RS, GPIO_OUT) # RS
#  GPIO_setup(LCD_D4, GPIO_OUT) # DB4
#  GPIO_setup(LCD_D5, GPIO_OUT) # DB5
#  GPIO_setup(LCD_D6, GPIO_OUT) # DB6
#  GPIO_setup(LCD_D7, GPIO_OUT) # DB7

  # Initialise display
  lcd_init()

  while True:

    # Send some test
    lcd_string("OrangePi 2G-IOT",LCD_LINE_1)
    lcd_string("16x2 LCD Test",LCD_LINE_2)

    time.sleep(3) # 3 second delay

    # Send some text
    lcd_string(message[0],LCD_LINE_1)
    lcd_string("",LCD_LINE_2)
    if (len(message) == 2):
      lcd_string(message[1],LCD_LINE_2)

    time.sleep(3) # 3 second delay

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.LCD_RS.write(mode) # RS

  # High bits
  GPIO.LCD_D4.write(False)
  GPIO.LCD_D5.write(False)
  GPIO.LCD_D6.write(False)
  GPIO.LCD_D7.write(False)
  if bits&0x10==0x10:
    GPIO.LCD_D4.write(True)
  if bits&0x20==0x20:
    GPIO.LCD_D5.write(True)
  if bits&0x40==0x40:
    GPIO.LCD_D6.write(True)
  if bits&0x80==0x80:
    GPIO.LCD_D7.write(True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.LCD_D4.write(False)
  GPIO.LCD_D5.write(False)
  GPIO.LCD_D6.write(False)
  GPIO.LCD_D7.write(False)
  if bits&0x01==0x01:
    GPIO.LCD_D4.write(True)
  if bits&0x02==0x02:
    GPIO.LCD_D5.write(True)
  if bits&0x04==0x04:
    GPIO.LCD_D6.write(True)
  if bits&0x08==0x08:
    GPIO.LCD_D7.write(True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.LCD_E.write(True)
  time.sleep(E_PULSE)
  GPIO.LCD_E.write(False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

if __name__ == '__main__':

  argv = sys.argv
  argc = len(argv)
  if (argc == 1):
    print 'Usage: python %s line1_message [line2_message]' % argv[0]
    quit()

  message = []
  message.append(argv[1])
  if (argc == 3):
    message.append(argv[2])
#  print message

  try:
    main(message)
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
#    GPIO_cleanup()
