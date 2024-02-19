import time


class dh_manager:
    def __init__(self,dht_device):
         self.dht_device= dht_device
    def get_values(self):
            try:
                temperature = self.dht_device.temperature
                humidity = self.dht_device.humidity
            except RuntimeError as err:
                print(err.args[0])
                return None, None

            return temperature, humidity