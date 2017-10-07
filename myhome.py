import argparse
import datetime
import time
from temperature import ds18b20
from switch import onoff
from scheduler import schedbase


MIN_TEMPERATURE_C = 10
TEMP_HYSTERESIS = 1

REFRESH_INTERVAL = 15

## Expected temperature json format:
## 
## {"mon":[
##         {"start":"12:10",
##          "finish":"15:15",
##          "attr":{"temp_c":10}},
##         {"start":"16:10",
##          "finish":"17:15",
##          "attr":{"temp_c":10}}
##        ]
## }

parser = argparse.ArgumentParser(description='My home automation.')
parser.add_argument('--temperature-schedule', metavar='json', type=str,
                    help='Temperature schedule, this is both a read and write pointer.')

args = parser.parse_args()


## compare_hyst_lt
#    Compare with hysteresis
def compare_hyst_lt(less, more):
    if (float(less)+float(TEMP_HYSTERESIS)) < more:
        return True
    return False

def compare_hyst_gt(more, less):
    if (float(more)-float(TEMP_HYSTERESIS)) > less:
        return True
    return False

## temp_control
#    Main temperature control loop
def temp_control(current_time, current_temperature, temp_sched, boiler_state):

    # Current_target will be none if nothing is scheduled for the current time,
    # otherwise it will return a dict with relevant keys
    current_target = max([x['temp_c'] for x in temp_sched.get_attr_from_time(current_time)]+[MIN_TEMPERATURE_C])
    if compare_hyst_lt(current_temperature, current_target):
        boiler_state.set_on()
        return 0
    elif compare_hyst_gt(current_temperature, current_target):
        boiler_state.set_off()
        return 0

    return 0


temp_attr = {
    'mandatory':('temp_c'),
    'optional':None
}

temp_sched = schedbase.SchedBase(attr=temp_attr)
if args.temperature_schedule:
    temp_sched.read_file(args.temperature_schedule)

boiler_state = onoff.OnOff()
boiler_state.set_off() ## for start up safety

temp_obj = ds18b20.ds18b20()

## Main loop
while(True):
    current_time = datetime.datetime.now().time()
    current_temperature = temp_obj.read_c()
    ## Temperature control
    print (current_temperature)
    temp_control(current_time, current_temperature, temp_sched, boiler_state)

    time.sleep(REFRESH_INTERVAL)


