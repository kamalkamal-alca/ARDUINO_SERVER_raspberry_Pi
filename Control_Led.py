import RPi.GPIO as GPIO
import time
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # DEVICE_ID
SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # SECRET_KEY

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for the LEDs
LED1 = 14
LED2 = 15

# Remove duplicate GPIO setup
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

# Initialize LEDs to low (off)
GPIO.output(LED1, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)

# Callback functions (unchanged)
def on_led_changed1(client, value):
    if value:  
        GPIO.output(LED1, GPIO.HIGH)
    else:
        GPIO.output(LED1, GPIO.LOW)
    print("LED1 change! Status is: ", value)

def on_led_changed2(client, value):
    if value:  
        GPIO.output(LED2, GPIO.HIGH)
    else:
        GPIO.output(LED2, GPIO.LOW)
    print("LED2 change! Status is: ", value)

if __name__ == "__main__":
    try:
        # Create the Arduino Cloud Client
        client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

        # Register the variables with the client
        client.register("led1", value=None, on_write=on_led_changed1)
        client.register("led2", value=None, on_write=on_led_changed2)

        # Start the client to listen for updates
        client.start()

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
