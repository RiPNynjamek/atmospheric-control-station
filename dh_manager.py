import adafruit_dht
import board
import RPi.GPIO as GPIO
import logging
from datetime import datetime
import time

# logging.basicConfig(level=logging.INFO)

class dh_manager:
    def __init__(self): 
        self.dht_device= adafruit_dht.DHT22(board.D4) # D4 = pin 4 in BCM mode 
        self.fan_port = 18
        self.humid_port = 17
        self.fan_on = False
        self.humidifier_on = False

        self.config = self.read_config()

        # GPIO initialization
        try:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.fan_port, GPIO.OUT)
            GPIO.setup(self.humid_port, GPIO.OUT)
            GPIO.output(self.humid_port, GPIO.HIGH)
            GPIO.output(self.fan_port, GPIO.HIGH)
        except Exception as e:
            logging.error(f"Error during initialization: {e}")
            GPIO.cleanup()
            raise
        

    def get_values(self):
        temperature = None
        humidity = None
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity
        except Exception as err:
            raise err
        return temperature, humidity

    def manage_climate(self):
        temperature, humidity = self.get_values()
        
        # TESTING PURPOSES
        # humidity = int(input('Enter humidity: '))
        # temperature = int(input('Enter temperature: '))

        if temperature is None or humidity is None:
            return None, None
        logging.info(f"temperature :{temperature:.1f} C | humidity:{humidity}%")

        # FAN ONLY LOGIC
        start_time = time.time()
        duration_high_temp = 50  # Durée en secondes
        duration_high_humid = 10

        if temperature > self.config.get('max_temperature') or humidity > self.config.get('max_humidity'):
            while temperature is None or temperature > self.config.get('ideal_temperature') or time.time() - start_time < duration_high_temp:
                logging.info('Temperature above ideal : {}°C'.format(temperature))
                self.control_fan(True)
                time.sleep(2)
                temperature, humidity = self.get_values()

            while humidity is None or humidity > self.config.get('ideal_humidity') or time.time() - start_time < duration_high_humid:
                logging.info('Humidity above ideal : {}%'.format(humidity))
                self.control_fan(True)
                time.sleep(2)
                temperature, humidity = self.get_values()
        self.control_fan(False) # disable fan after temp/humidity reduction
        
        ## FAN & HUMIDIFIER LOGIC
        # # Handle high temperature
        # if temperature > self.config.get('max_temperature'):
        #     logging.info('Temperature above maximum : {}°'.format(temperature))
        #     self.control_fan(True) #fan turned on to cool down the air
        #     self.control_humidifier(False) #turn off humidifier since the fan will dry the air anyways, waste of water
        #     return temperature, humidity, self.fan_on, self.humidifier_on
        # else:
        #     if humidity >= self.config.get('ideal_humidity'):
        #         logging.info('Humidity above normal : {}%'.format(humidity))
        #         self.control_humidifier(False) # turn off the humidifier
                
        #         # if temperature > self.config.get('max_temperature'):
        #         #     self.control_fan(True) #fan turned on to cool down the air
        #         return temperature, humidity, self.fan_on, self.humidifself.fan_portconfigier_on
            
        #     if humidity <= self.config.get('min_humidity'):
        #         logging.info('Humidity below normal : {}%'.format(humidity))
        #         self.control_humidifier(True) # turn on the humidifier

        #         # if(temperature < self.config.get('max_temperature')):
        #         #     self.control_fan(False) #disable the fan if the temperature is fine to let relative humidity ramp up

        #         return temperature, humidity, self.fan_on, self.humidifier_on

        # Default state: fan and humidifier off if no conditions met
        # self.control_fan(False)
        # self.control_humidifier(False)
        logging.info(f"Climate is stable.")
        return temperature, humidity, self.fan_on, self.humidifier_on

    def control_fan(self, state):
        if getattr(self, 'fan_on', None) != state:  # Check current state
            GPIO.output(self.fan_port, GPIO.LOW if state else GPIO.HIGH)
            self.fan_on = state  # Store current state
            logging.info('Fan started.' if state else 'Fan stopped.')

    def control_humidifier(self, state):
        if getattr(self, 'humidifier_on', None) != state:  # Check current state
            GPIO.output(self.humid_port, GPIO.LOW if state else GPIO.HIGH)
            self.humidifier_on = state  # Store current state
            logging.info('Humidifier started.' if state else 'Humidifier stopped.')


    def read_config(self, file_path='configuration.txt'):
        self.config = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Strip whitespace and skip empty lines or comments
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    # Split each line into key and value
                    try:
                        key, value = line.split('=')
                        self.config[key.strip()] = float(value.strip())
                    except ValueError:
                        logging.error(f"Invalid line in config: {line}")       
        except FileNotFoundError:
            logging.error(f"Error: The file {file_path} does not exist.")
        return self.config
    
    def cleanup(self):
        self.control_humidifier(False)
        self.control_fan(False)
        # GPIO.output(self.humid_port, GPIO.HIGH)
        time.sleep(2) # hardware limitations: 2s after an error
        # GPIO.output(self.fan_port, GPIO.HIGH)
        GPIO.cleanup()
        logging.info("GPIO resources cleaned up.")