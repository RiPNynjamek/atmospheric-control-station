import unittest
import time
from dh_manager import dh_manager


"""Set up the dh_manager instance and initialize GPIO."""
dh = dh_manager()
# dh.fan_port = 18  # Use actual GPIO pins
# dh.humid_port = 6
dh.initialize()

try:
    print("Turning fan ON")
    dh.control_fan(True)
    time.sleep(5)

    print("Turning fan OFF")
    dh.control_fan(False)
    time.sleep(5)

    print("Turning humidifier ON")
    dh.control_humidifier(True)
    time.sleep(5)

    print("Turning humidifier OFF")
    dh.control_humidifier(False)
    time.sleep(5)

except KeyboardInterrupt:
    print("Interrupted by user")    
finally:
    dh.cleanup()