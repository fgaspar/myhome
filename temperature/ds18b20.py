from temperature import tempbase
from w1thermsensor import W1ThermSensor

class ds18b20(tempbase.TempBase):
    def __init__ (self):
        super().__init__()
        sensor = W1ThermSensor()

    ## read_c
    #   Returns the temeprature in 1/1000 degrees C
    def read_c(self):
        # Read sensor and return an integer corresponding to 1/1000 degrees c
        self.sensor.get_temperature()

