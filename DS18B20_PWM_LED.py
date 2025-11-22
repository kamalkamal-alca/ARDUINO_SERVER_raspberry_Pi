import RPi.GPIO as GPIO
import time
from arduino_iot_cloud import ArduinoCloudClient
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

DEVICE_ID = "222222222222222222222"  # Remove the 'b' prefix
SECRET_KEY = "aaaaaaaaaaaaaaaaaaaa"  # Remove the 'b' prefix

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for the LEDs
LED1 = 14
LED2 = 15
PWM_PIN = 12  # GPIO12, not 18 as mentioned in comment

# Remove duplicate GPIO setup
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, 1000)
pwm.start(0)

# Initialize LEDs to low (off)
GPIO.output(LED1, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)

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
        client.register("temperatureC", on_read=read_temperature, interval=10.0)
        client.register("temperatureF", on_read=read_temperatureF, interval=10.0)
        client.register("led1", value=None, on_write=on_led_changed1)
        client.register("led2", value=None, on_write=on_led_changed2)
        client.register("pwm", value=None, on_write=on_led_changed3)

        # Start the client to listen for updates
        client.start()

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Clean up GPIO on exit
        pwm.stop()
        GPIO.cleanup()
