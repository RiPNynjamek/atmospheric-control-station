import dh_manager
import time
import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D4) # D4 = pin 4 in BCM mode 
dh = dh_manager.dh_manager(dht_device)

while True: # while true loop because why the fuck not
    temperature, humidity = dh.get_values()
    if temperature is None or humidity is None:
        print("Invalid readout, waiting for a valid one") # the sensor sometimes fails to retrieve a value so needed a safeguard
        continue
    print("Temp:{:.1f} C          Humidity:{}%".format(temperature,humidity))
    time.sleep(2)