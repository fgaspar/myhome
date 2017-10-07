from temperature import tempbase

class ds18b20(tempbase.TempBase):
    def __init__ (self):
        pass
        ## open any required connections to sensor
    ## read_c
    #   Returns the temeprature in 1/1000 degrees C
    def read_c(self):
        # Read sensor and return an integer corresponding to 1/1000 degrees c
        ##TODO fix this
        return 12

