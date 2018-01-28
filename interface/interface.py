import datetime
import Adafruit_CharLCD as LCD


VALID_STATES = [
    "DEFAULT",
    "SET_MIN_TEMP",
    "SET_EXTRA_TIME",
    "SET_EXTRA_TEMP",
    "SET_ON_TEMP",
    "SCHEDULE",
    "NAVIGATION"
]

OPTION_ORDER = [
    "SCHEDULE",
    "SET_MIN_TEMP",
    "SET_EXTRA_TIME",
    "SET_EXTRA_TEMP",
    "SET_ON_TEMP"
]

MAX_TEMP = 40
MIN_TEMP = -9

LONG_PRESS_TIME = datetime.timedelta(seconds = 0.75)
BUTTONS_UPDATE_TIME = 0.1 #Seconds

TEMPERATURE_CHAR = [
    0B00100,
    0B01010,
    0B01010,
    0B01110,
    0B01110,
    0B11111,
    0B11111,
    0B01110
]

ARROW_UP = [
    0B00000,
    0B00100,
    0B01110,
    0B11111,
    0B01110,
    0B01110,
    0B01110,
    0B00000
]

ARROW_DOWN = [
    0B00000,
    0B01110,
    0B01110,
    0B01110,
    0B11111,
    0B01110,
    0B00100,
    0B00000
]

ARROW_LEFT = [
    0B00000,
    0B00000,
    0B00100,
    0B00110,
    0B11111,
    0B00110,
    0B00100,
    0B00000
]

ARROW_RIGHT = [
    0B00000,
    0B00000,
    0B00100,
    0B01100,
    0B11111,
    0B01100,
    0B00100,
    0B00000
]


class Interface(object):
    def __init__(self):
        self.force_update = True 

        self.lcd            = LCD.Adafruit_CharLCDPlate()
        self.lcd.set_color(0.0, 0.0, 1.0)
        self.lcd.set_backlight(1)

        self.current_menu = "DEFAULT"
        self.current_state = {}
        self.option_str_method = {
            "SET_MIN_TEMP":  {"str": "Set min. temp.", "method":self._set_min_temp},
            "SET_EXTRA_TIME":{"str": "Set xtra time",  "method":self._set_extra_time},
            "SET_EXTRA_TEMP":{"str": "Set xtra temp.", "method":self._set_extra_temp},
            "SET_ON_TEMP":   {"str": "Set ON temp.",   "method":self._set_on_temp},
            "SCHEDULE":      {"str": "Config. sched.", "method":self._schedule}
            "DEFAULT":       {"str": "",               "method":self._default}
        }

        init_date = datetime.now() - LONG_PRESS_TIME
        # Button state
        self.buttons = {
            'left' : {'ID':LCD.LEFT,   'pressed': False, 'long': False, 'last_press': init_date, 'read':False, 'last_read': init_date},
            'right': {'ID':LCD.RIGHT,  'pressed': False, 'long': False, 'last_press': init_date, 'read':False, 'last_read': init_date},
            'up'   : {'ID':LCD.UP,     'pressed': False, 'long': False, 'last_press': init_date, 'read':False, 'last_read': init_date},
            'down' : {'ID':LCD.DOWN,   'pressed': False, 'long': False, 'last_press': init_date, 'read':False, 'last_read': init_date},
            'sel'  : {'ID':LCD.SELECT, 'pressed': False, 'long': False, 'last_press': init_date, 'read':False, 'last_read': init_date}
        }

    def _default(self, temp_sched, temp_obj, boiler_state):
        current_time_str    = datetime_now.strftime('%H'+t_sep+'%M')
        lcd_str = current_time_str + ' '*5 + '{: >05.1f}c'.format(global_temp['c']) + '\n'
        with boiler_state.lock:
            state = boiler_state.get_state()
        state = 'ON' if state else 'OFF'
        lcd_str = lcd_str + "{:>16}".format(state)

        # Store state
        self.current_state["menu"] = "DEFAULT"
        self.current_state["state"] = {}
        return lcd_str

    def _set_min_temp(self):
        current_min = TODO get_from_config('min_temp')
        saved = False
        if self.current_menu == "SET_MIN_TEMP":
            current_min = self.current_state["current_min"]
            saved = self.current_state["saved"]
        lcd_str = "Sel min temp." + '\n'
        lcd_str = lcd_str + '{: 05.1f}T'.format(current_min)

        if self.pressed('up'):
            saved = False
            if self.long_press('up'):
                current_min = current_min + 2
            else:
                current_min = current_min + 1

        if self.pressed('down'):
            saved = False
            if self.long_press('down'):
                current_min = current_min - 2
            else:
                current_min = current_min - 1

        if current_min > MAX_TEMP:
            current_min = MAX_TEMP

        if current_min < MIN_TEMP:
            current_min = MIN_TEMP

        if self.pressed('back'):
            self._navigation()

        if self.pressed('sel'):
            saved = True
            TODO set_config({'min_temp':current_min})

        if saved:
            lcd_str = lcd_str + TODO black S

        self.current_state["current_min"] = current_min
        self.current_state["saved"] = saved

        return lcd_str


    def _set_extra_time(self):

    def _set_extra_temp(self):

    def _set_on_temp(self):

    def _schedule(self):

    def _navigation(self):
        current_position = 0
        cursor_position = 0
        if self.current_menu == "NAVIGATION":
            current_position = self.current_state["current_position"]
            cursor_position = self.current_state["cursor_position"]

        lcd_str = ""
        for i in range(2):
            if cursor_position == i:
                TODO ## print special char
            else:
                lcd_str = lcd_str + " "
            arrow = ""
            if cursor_position == 0:
                arrow = TODO arrow up
            else:
                arrow = TODO arrow down
            effective_pos = (current_position + i)%len(OPTION_ORDER)
            lcd_str = lcd_str + self.option_str_method[OPTION_ORDER[effective_pos]]["str"] + arrow + '\n'

        effective_pos = (current_position + cursor_position)%len(OPTION_ORDER)
        if self.pressed('right'):
            self.option_str_method[OPTION_ORDER[effective_pos]]["method"]()

        if self.pressed('up'):
            if cursor_position == 1:
                current_position = (current_position+1)%len(OPTION_ORDER)
            else:
                cursor_position = cursor_position + 1

        if self.pressed('down'):
            if cursor_position == 0:
                current_position = (current_position-1+len(OPTION_ORDER))%len(OPTION_ORDER) # Extra len added for subtractin goblins
            else:
                cursor_position = cursor_position - 1

        if self.pressed('back'):
            self._default()

        self.current_menu = "NAVIGATION"
        self.current_state = {}
        self.current_state["current_position"] = current_position
        self.current_state["cursor_position"] = cursor_position

        return lcd_str

    def generate(self):
        self.option_str_method[current_menu]["method"]()


    ## Buttons interaction

    def pressed(button, single_press = True):
        if single_press and sum([self.buttons[x]['pressed'] for x in self.buttons])>1:
            return False
        if self.buttons[button]['pressed'] and not self.buttons[button]['read']:
            self.buttons[button]['read'] = True
            return True
        return False

    def long_press(button):
        return self.buttons[button]['long']

    ## Method to be called
    def update_button_state(self, repeat=None):
        go_around = True
        while go_around:
            for button in self.buttons:
                pressed = lcd.is_pressed(self.buttons[button]['ID'])
                if pressed:
                    if self.buttons[button]['pressed'] and datetime.now() - self.buttons[button]['last_press'] > LONG_PRESS_TIME:
                        self.buttons[button]['long'] = True
                    else:
                        self.buttons[button]['pressed'] = True
                        self.buttons[button]['last_press'] = datetime.now()
                else:
                    self.buttons[button]['pressed'] = False
                    self.buttons[button]['long'] = False
                    self.buttons[button]['read'] = False

            if repeat:
                sleep(repeat)
            else:
                go_around = False
