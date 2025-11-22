import RPi.GPIO as GPIO
import time
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "----------------------------------"  # DEVICE_ID
SECRET_KEY = "---------------------------------"  # SECRET_KEY
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for the LEDs
PWM_PIN = 12  # GPIO12, not 18 as mentioned in comment

# Remove duplicate GPIO setup
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, 1000)
pwm.start(0)

def on_led_changed3(client, value):
    try:
        pwm_value = int(value)
        if 0 <= pwm_value <= 100:
            pwm.ChangeDutyCycle(pwm_value)
            print(f"PWM duty cycle changed to: {pwm_value}%")
        else:
            print("Invalid PWM value. Provide a value between 0 and 100.")
    except ValueError:
        print("Invalid input for PWM. Must be a number.")

if __name__ == "__main__":
    try:
        # Create the Arduino Cloud Client
        client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

        # Register the variables with the client
        client.register("pwm", value=None, on_write=on_led_changed3)

        # Start the client to listen for updates
        client.start()

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Clean up GPIO on exit
        pwm.stop()
