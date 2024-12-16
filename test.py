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

    def test_control_fan_on(self):
        """Test turning the fan ON."""
        self.dh.control_fan(True)
        self.assertTrue(self.dh.fan_on)
        self.assertEqual(GPIO.input(self.dh.fan_port), GPIO.HIGH)

    def test_control_fan_off(self):
        """Test turning the fan OFF."""
        self.dh.control_fan(False)
        self.assertFalse(self.dh.fan_on)
        self.assertEqual(GPIO.input(self.dh.fan_port), GPIO.LOW)

    def test_control_humidifier_on(self):
        """Test turning the humidifier ON."""
        self.dh.control_humidifier(True)
        self.assertTrue(self.dh.humidifier_on)
        self.assertEqual(GPIO.input(self.dh.humid_port), GPIO.HIGH)

    def test_control_humidifier_off(self):
        """Test turning the humidifier OFF."""
        self.dh.control_humidifier(False)
        self.assertFalse(self.dh.humidifier_on)
        self.assertEqual(GPIO.input(self.dh.humid_port), GPIO.LOW)

if __name__ == "__main__":
    unittest.main()
