import dh_manager
import time
import adafruit_dht
import board
import RPi.GPIO as GPIO

dht_device = adafruit_dht.DHT22(board.D4) # D4 = pin 4 in BCM mode 
dh = dh_manager.dh_manager(dht_device)
fan_port = 18
humid_port = 6
max_temperature = 28
min_temp = 18
min_humidity = 50
max_humidity = 60
time.sleep(5) # need to wait for sensor initialization

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_port, GPIO.OUT)
GPIO.setup(humid_port, GPIO.OUT)

while True: # while true loop because why the fuck not
    temperature, humidity = dh.get_values()
    if temperature is None or humidity is None:
        print("Invalid readout, waiting for a valid one") # the sensor sometimes fails to retrieve a value so needed a safeguard
        continue

    if temperature >= max_temperature:
        GPIO.output(fan_port,GPIO.HIGH) #fan turned on to cool down the air
        GPIO.output(humid_port,GPIO.LOW) #turn off humidifier since the fan will dry the air anyways, waste of water
        time.sleep(300) # let the fan run for 5 minutes should be enough to cool down the air.
    else:
        GPIO.output(fan_port,GPIO.LOW) 

    if humidity >= max_humidity:
        GPIO.output(humid_port, GPIO.LOW)
    
    if humidity <= min_humidity:
        GPIO.output(humid_port, GPIO.HIGH)
        GPIO.output(fan_port,GPIO.LOW) #disable the fan to let relative humidity ramp up
        time.sleep(300) # wait 5 minutes so the humidity goes back up
    print("Temp:{:.1f} C          Humidity:{}%".format(temperature,humidity))
    time.sleep(30) # 30s between 2 readings in production