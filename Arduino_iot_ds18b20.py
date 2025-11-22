import time
from arduino_iot_cloud import ArduinoCloudClient
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

DEVICE_ID = "------------------------------"  # DEVICE_ID
SECRET_KEY = "-----------------------------"  # SECRET_KEY

# Function to read temperature
def read_temperature(client):
    temperature = sensor.get_temperature()
    if temperature is not None:
        print(f'Temperature: {temperature:.1f}*C')
        return temperature
    else:
        print("Failed to retrieve temperature data from the sensor")
        return None

# Function to read temperatureF
def read_temperatureF(client):
    temperature = sensor.get_temperature()
    temperatureF  = temperature  * 9.0 / 5.0 + 32.0
    if temperature is not None:
        print(f'Temperature: {temperatureF:.1f}*C')
        return temperature
    else:
        print("Failed to retrieve temperature data from the sensor")
        return None

if __name__ == "__main__":
    try:
        # Create the Arduino Cloud Client
        client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

        # Register the variables with the client
        client.register("temperatureC", on_read=read_temperature, interval=10.0)
        client.register("temperatureF", on_read=read_temperatureF, interval=10.0)

        # Start the client to listen for updates
        client.start()

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Clean up GPIO on exit
        sensor.stop()
