class Entry(object):
    def __init__(self, start_time, finish_time, attr = None):
        if attr:
            if isinstance(attr, dict):
                self.attr = attr
            else:
                raise RuntimeError('Unexpected type for attr, should be dict')
        else:
            self.attr = dict()
        self.start_time = start_time
        self.finish_time = finish_time

    def set_finish_time(self, finish_time):
        self.finish_time = finish_time

    def set_start_time(self, path, format=None):
        self.start_time = start_time

    def get_start(self):
        return self.start_time

    def get_finish(self):
        return self.finish_time

    def __str__(self):
        print ('Event from {} to {} with attr {}.'.format(self.start_time, self.finish_time, self.attr))