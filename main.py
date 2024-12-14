import dh_manager
import time
import adafruit_dht
import board
import RPi.GPIO as GPIO
import csv
from datetime import datetime
import matplotlib.pyplot as plt


dht_device = adafruit_dht.DHT22(board.D4) # D4 = pin 4 in BCM mode 
dh = dh_manager.dh_manager(dht_device)
fan_port = 18
humid_port = 6
max_temperature = 28
ideal_temperature = 24
min_temp = 18
min_humidity = 50
max_humidity = 60
ideal_humidity = 55
time.sleep(5) # need to wait for sensor initialization

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_port, GPIO.OUT)
GPIO.setup(humid_port, GPIO.OUT)
fields = ['Date','Temperature','Humidity']
values = []
while True: # while true loop because why the fuck not
    temperature, humidity = dh.get_values()
    values.append({'Date':datetime.now(),'Temperature':temperature,'Humidity':humidity})
    if temperature is None or humidity is None:
        print("Invalid readout, waiting for a valid one") # the sensor sometimes fails to retrieve a value so needed a safeguard
        continue
    print("Temp:{:.1f} C          Humidity:{}%".format(temperature,humidity))

    if temperature >= max_temperature:
        print('Temperature above normal : {}°'.format(temperature))
        updatedTemp, updatedHumid = dh.get_values()

        while(updatedTemp > ideal_temperature):
            GPIO.output(fan_port,GPIO.HIGH) #fan turned on to cool down the air
            GPIO.output(humid_port,GPIO.LOW) #turn off humidifier since the fan will dry the air anyways, waste of water
            updatedTemp, updatedHumid = dh.get_values()

            values.append({'Date':datetime.now(),'Temperature':updatedTemp,'Humidity':updatedHumid})
            print('Fan running. Current temperature:{:.1f} C ; current humidity:{}%'.format(updatedTemp,updatedHumid))
            time.sleep(30) # let the fan run for 30s and check temperature & humidity again.
        GPIO.output(fan_port,GPIO.LOW) #turn off the fan when temperature is ok
    else:
        GPIO.output(fan_port,GPIO.LOW) #turn off the fan if temperature is ok




    if humidity >= max_humidity:
        print('Humidity above normal : {}%'.format(humidity))
        updatedTemp, updatedHumid = dh.get_values()
        GPIO.output(humid_port, GPIO.LOW) # turn off the humidifier
        while(updatedTemp > ideal_temperature):
            updatedTemp, updatedHumid = dh.get_values()
            values.append({'Date':datetime.now(),'Temperature':updatedTemp,'Humidity':updatedHumid})
            if(updatedTemp > ideal_temperature):
                GPIO.output(fan_port,GPIO.HIGH) #fan turned on to cool down the air

            print('Fan running. Current temperature:{:.1f} C ; current humidity:{}%'.format(updatedTemp,updatedHumid))
            time.sleep(30) # let the fan run for 30s and check temperature & humidity again.
    
    if humidity <= min_humidity:
        print('Humidity below normal : {}%'.format(humidity))
        updatedTemp, updatedHumid = dh.get_values()
        GPIO.output(humid_port, GPIO.HIGH)

        while(updatedHumid <= max_humidity):
            updatedTemp, updatedHumid = dh.get_values()
            values.append({'Date':datetime.now(),'Temperature':updatedTemp,'Humidity':updatedHumid})
            GPIO.output(humid_port, GPIO.HIGH)
            GPIO.output(fan_port,GPIO.LOW) #disable the fan to let relative humidity ramp up
            print('Humidifier running. Current temperature:{:.1f} C ; current humidity:{}%'.format(updatedTemp,updatedHumid))
            time.sleep(30) # wait 30s between next humidity readout

    with open('readings.txt', 'w') as f:
        f.write('Temp:{:.1f} C          Humidity:{}%'.format(temperature,humidity))

    with open('data.csv','w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()
        writer.writerows(values)
    time.sleep(30) # 30s between 2 readings in production