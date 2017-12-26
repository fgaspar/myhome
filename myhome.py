import argparse
import datetime
import time
import threading
from temperature import ds18b20
from switch import onoff
from scheduler import schedbase
import Adafruit_CharLCD as LCD


MIN_TEMPERATURE_C = 10
TEMP_HYSTERESIS = 1
TEMP_REFRESH_INTERVAL = 2

REFRESH_INTERVAL_INTERNAL   = 15
REFRESH_INTERVAL_CONTROLLER = 0.5

## LCD
NUM_DIFF_UPDATE = 10
LCD_SLEEP_TIME = 10
LCD_LINE_SIZE = 16

##Relay
BCM_RELAY_PIN = 16

BUTTONS = (LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT)

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

###########################
## Arguments
###########################

parser = argparse.ArgumentParser(description='My home automation.')
parser.add_argument('--temperature-schedule', metavar='json', type=str,
                    help='Temperature schedule, this is both a read and write pointer.')

args = parser.parse_args()


###########################
## LCD Interface
###########################
def interface(temp_sched, temp_obj, boiler_state):
    lcd            = LCD.Adafruit_CharLCDPlate()
    lcd.set_color(0.0, 0.0, 1.0)
    lcd.set_backlight(1)

    prev_lcd_str  = ""
    in_use         = True
    button_lock    = False
    button_press   = []
    time_prev_use  = datetime.datetime.now()
    while True :
        datetime_now        = datetime.datetime.now()
        t_sep               = ':' if datetime_now.second % 2 == 0 else ' '
        current_time_str    = datetime_now.strftime('%H'+t_sep+'%M')
        button_press        = [i for i in BUTTONS if lcd.is_pressed(i)]
        if not in_use and button_press:
            in_use      = True
            button_lock = True
            lcd.set_backlight(1)
        if button_press:
            time_prev_use = datetime_now
        if button_lock and not button_press:
            button_lock = False
        lcd_str = current_time_str + ' '*5 + '{: >05.1f}c'.format(global_temp['c']) + '\n'
        with boiler_state.lock:
            state = boiler_state.get_state()
        state = 'ON' if state else 'OFF'
        lcd_str = lcd_str + "{:>16}".format(state)
        update_lcd(lcd, lcd_str, prev_lcd_str)
        prev_lcd_str = lcd_str

        if datetime_now - time_prev_use > datetime.timedelta(seconds=LCD_SLEEP_TIME):
            in_use = False
            lcd.set_backlight(0)
        if not in_use:
            time.sleep(REFRESH_INTERVAL_CONTROLLER)

def update_lcd(lcd, text, text_prev):
    if (len(text) != len(text_prev)) or \
            (sum([text[i]!=text_prev[i] for i in range(len(text_prev))]) > NUM_DIFF_UPDATE):
        lcd.clear()
        lcd.message(text)
    else:
        text_clean = text.replace('\n', '')
        text_prev_clean = text_prev.replace('\n', '')
        for i, c in enumerate(text_clean):
            if i<len(text_prev) and c != text_prev_clean[i]:
                lcd.set_cursor(i % LCD_LINE_SIZE, i//LCD_LINE_SIZE)
                lcd.message(c)

###########################
## Background updates
###########################
def update_global_temp_c(global_temp, temp_obj):
    while True:
        global_temp['c'] = temp_obj.read_c()
        time.sleep(TEMP_REFRESH_INTERVAL)


###########################
## Helper for main control
###########################

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
    print('Current target: {}'.format(current_target))

    if compare_hyst_lt(current_temperature, current_target):
        boiler_state.set_on()
        return 0
    elif compare_hyst_gt(current_temperature, current_target):
        boiler_state.set_off()
        return 0

    return 0


###########################
## Setup
###########################

temp_attr = {
    'mandatory':('temp_c'),
    'optional':None
}

temp_sched = schedbase.SchedBase(attr=temp_attr)
if args.temperature_schedule:
    temp_sched.read_file(args.temperature_schedule)

boiler_state = onoff.OnOff(BCM_RELAY_PIN)
boiler_state.set_off() ## for start up safety

temp_obj = ds18b20.ds18b20()

## This must be a reference due to the update in threading, a dict will do
global_temp = {'c':temp_obj.read_c()}

## Start helper threads

# Print LCD
lcd_controller = threading.Thread(target=interface, args=(temp_sched, global_temp, boiler_state))
lcd_controller.daemon = True
lcd_controller.start()

# Temperature read out
temp_update = threading.Thread(target=update_global_temp_c, args=(global_temp, temp_obj))
temp_update.daemon = True
temp_update.start()

# Schedule read

# Menu tracking

###########################
## Main loop
###########################

while(True):
    datetime_now = datetime.datetime.now()
    current_time = datetime_now.time()
    with temp_obj.lock:
        current_temperature = temp_obj.read_c()
    ## Temperature control
    print (current_temperature)
    with temp_sched.lock, boiler_state.lock:
        temp_control(current_time, current_temperature, temp_sched, boiler_state)

    time.sleep(REFRESH_INTERVAL_INTERNAL)


