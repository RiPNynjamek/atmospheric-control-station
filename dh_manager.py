class dh_manager: # no need for a class in my usecase but I created one anyways because i'm a madman
    def __init__(self,dht_device): 
         self.dht_device= dht_device
    def get_values(self):
        temperature = None
        humidity = None
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity
        except RuntimeError as err:
            print(err.args[0])

        return temperature, humidity