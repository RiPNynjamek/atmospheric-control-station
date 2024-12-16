import unittest
import RPi.GPIO as GPIO
from dh_manager import dh_manager

class TestDhManagerGPIO(unittest.TestCase):
    def setUp(self):
        """Set up the dh_manager instance and initialize GPIO."""
        self.dh = dh_manager()
        self.dh.fan_port = 18  # Use actual GPIO pins
        self.dh.humid_port = 6
        GPIO.setmode(GPIO.BCM)  # Use BCM numbering
        GPIO.setup(self.dh.fan_port, GPIO.OUT)
        GPIO.setup(self.dh.humid_port, GPIO.OUT)

    def tearDown(self):
        """Clean up GPIO resources after each test."""
        GPIO.cleanup()

    def test_control_fan(self):
        while True:
            temperature = int(input('Enter temperature: '))
            """Test turning the fan ON."""
            if(temperature > 25):
                self.dh.control_fan(True)
            else:
                self.dh.control_fan(False)

    # def test_control_humidifier(self):
    #     while True:
    #         humidity = int(input('Enter humidity: '))
    #         """Test turning the fan ON."""
    #         if(humidity > 50):
    #             self.dh.control_humidifier(True)
    #         else:
    #             self.dh.control_humidifier(False)


if __name__ == "__main__":
    unittest.main()
