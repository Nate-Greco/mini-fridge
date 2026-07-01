from gpiozero import Servo
import time
import pigpio

pi = pigpio.pi()

pin = 18
refresh = 333
dead = 2

middle = 1500
mini = 500
maxi = 2500


pi.set_PWM_frequency(pin, refresh)

while True:
	pi.set_servo_pulsewidth(pin,  mini)
	time.sleep(0.5)
	pi.set_servo_pulsewidth(pin,  middle)
	time.sleep(0.5)
	pi.set_servo_pulsewidth(pin,  maxi)
	time.sleep(0.5)
	time.sleep(0.5)
