import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
# GPIO.output(12, GPIO.LOW) NC is closed, NO is open
# GPIO.output(12, GPIO.HIGH) NO is open, NC is closed