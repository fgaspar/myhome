from switch import switch
import RPi.GPIO as GPIO

class OnOff(switch.Switch):
    def __init__(self, bcm_pin, attr = None):
        super().__init__(attr = attr)
        self.bcm_pin = bcm_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bcm_pin, GPIO.OUT)

    def set_on(self):
        self._set_on()
        GPIO.output(self.bcm_pin, GPIO.HIGH)

    def set_off(self):
        self._set_off()
        GPIO.output(self.bcm_pin, GPIO.LOW)
