import time
from ds18b20 import DS18B20
import RPi.GPIO as GPIO

sensor_ids = DS18B20.get_available_sensors()

relayPeltier = 12
relayFan = 16
goalTemp = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPeltier, GPIO.OUT)
GPIO.setup(relayFan, GPIO.OUT)


# GPIO.output(relayPeltier, GPIO.LOW) NC is closed, NO is open
# GPIO.output(relayPeltier, GPIO.HIGH) NO is open, NC is closed
# GPIO.output(relayFan, GPIO.LOW) NC is closed, NO is open
# GPIO.output(relayFan, GPIO.HIGH) NO is open, NC is closed

if not sensor_ids:
    print("No sensors")
else:
    print(f"Found sensor: {sensor_ids[0]}")
    sensor = DS18B20(sensor_ids[0])      
    while True:
        temperature = sensor.get_temperature()
        if temperature < goalTemp:
            GPIO.output(relayPeltier, GPIO.HIGH)
            GPIO.output(relayFan, GPIO.HIGH)
        else:
            GPIO.output(relayPeltier, GPIO.LOW)
            GPIO.output(relayFan, GPIO.LOW)
        print(temperature)
        time.sleep(0.01)
