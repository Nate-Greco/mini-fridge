import time
from ds18b20 import DS18B20

try:
    # Safely look for available hardware IDs first
    sensor_ids = DS18B20.get_available_sensors()
    
    if not sensor_ids:
        print("❌ Error: No DS18B20 sensors detected! Check your wiring and resistor.")
    else:
        print(f"✅ Found sensor: {sensor_ids[0]}")
        # Initialize using the confirmed sensor ID
        sensor = DS18B20(sensor_ids[0])
        
        while True:
            temperature = sensor.get_temperature()
            print(f"Temperature: {temperature:.2f}°C")
            time.sleep(1)

except KeyboardInterrupt:
    print("\nScript stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
