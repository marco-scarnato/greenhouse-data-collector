import RPi.GPIO as GPIO
from time import sleep
import sys

GPIO.setmode(GPIO.BCM)

sec = int(sys.argv[1])
gpio = int(sys.argv[2]) or 18

GPIO.setup(gpio, GPIO.OUT)

try:
	GPIO.output(gpio, GPIO.LOW)
	sleep(0.25)

	GPIO.output(gpio, GPIO.HIGH)
	sleep(sec)
	GPIO.cleanup()

except KeyboardInterrupt:
	GPIO.cleanup()
