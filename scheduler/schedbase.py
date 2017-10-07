import datetime
from datetime import date
import time
import json

from scheduler import entry


## Valid keys for use in day
SCHED_ALLOWED_DAYS = ('mon',
                      'tue',
                      'wed',
                      'thu',
                      'fri',
                      'sat',
                      'sun',
                      'all')

NUM_2_DAY          = {1:'mon',
                      2:'tue',
                      3:'wed',
                      4:'thu',
                      5:'fri',
                      6:'sat',
                      7:'sun'}

class SchedBase(object):
    def __init__(self, attr = None):
        if attr:
            if isinstance(attr, dict):
                self.attr = attr
            else:
                raise RuntimeError('Unexpected type for attr, should be dict')
        else:
            self.attr = dict()
        self.sched = {i:[] for i in SCHED_ALLOWED_DAYS}
        self.mandatory_attr = self.attr.get('mandatory_attr')
        self.optional_attr = self.attr.get('optional_attr')



    ## set_from_int
    #   Sets a new entry given an interval
    #   If no day is specified defaults to all
    def set_from_int(self, start, finish, attr, day=None):
        if ( day is not None ) and ( day not in SCHED_ALLOWED_DAYS) :
            raise RuntimeError('{} is not a valid day selection, please select a day from {}').format(day, SCHED_ALLOWED_DAYS)
        if day is None:
            day = 'all'
        if self.mandatory_attr is not None:
            for key in self.mandatory_attr:
                if key not in attr:
                    return 1
        sched[day].append(Entry(start, finish, attr=attr))

    ## read_file
    #   Appends a schedule based on a file read at [path]
    def read_file(self, path):
        with open(path, 'r') as fp:
            raw = json.load(fp)
        if any(not (key in SCHED_ALLOWED_DAYS) for key in raw):
            return 1
        sched = {i:[] for i in raw}
        for day in raw:
            for event in raw[day]:
                start = datetime.datetime.strptime(event['start'], '%H:%M').time()
                finish = datetime.datetime.strptime(event['finish'], '%H:%M').time()
                sched[day].append(entry.Entry(start, finish, attr=event['attr']))
                if self.mandatory_attr is not None:
                    for key in self.mandatory_attr:
                        if key not in entry.attr:
                            return 1

        for day in sched:
            self.sched[day] += sched[day]

        return 0

    ## save_file
    #   Saves a schedule to a file at [path]
    def save_file(self, path, format=None):
        raise NotImplementedError('save_file not implemented for class {}').format(self.__class__.__name__)
        ##json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4)

    def get_attr_from_time(self, time):
        to_return = [event.attr for event in sorted(self.sched[NUM_2_DAY[date.today().isoweekday()]] + self.sched['all'],
                                          key=entry.Entry.get_start)
            if (event.get_start() <= time and time < event.get_finish()) ]
        return to_return

    ## delete_interval
    #   Deletes the interval that starts at or contains time
    #   Returns 0 on success, returns 1 is there is no such interval
    def delete_interval(self, time):
        raise NotImplementedError('delete_interval not implemented for class {}').format(self.__class__.__name__)

    def __str__(self):
        print ('Using {} scheduler.'.format(self.__class__.__name__))