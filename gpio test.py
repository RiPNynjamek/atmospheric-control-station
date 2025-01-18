import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
relay_pin = 17  # Adjust based on your GPIO pin

GPIO.setup(relay_pin, GPIO.OUT)

# Toggle relay
while True:
    GPIO.output(relay_pin, GPIO.HIGH)  # Turn on relay
    time.sleep(2)
    GPIO.output(relay_pin, GPIO.LOW)   # Turn off relay
    time.sleep(2)