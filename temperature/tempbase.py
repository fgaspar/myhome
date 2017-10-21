import threading

class TempBase(object):
    def __init__(self):
        self.lock = threading.Lock()
        pass
    ## read_c
    #   Returns the temeprature in 1/1000 degrees C
    def read_c(self):
        raise NotImplementedError('read_c not implemented for class {}').format(self.__class__.__name__)

    def __str__(self):
        print ('Current temperature: {} C'.format(self.read_c()/1000))