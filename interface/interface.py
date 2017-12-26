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
    def __init__(self, lcd):
        force_update = True 
        lcd = lcd
        current_menu = "DEFAULT"
        current_state = {}
        option_str_method = {
            "SET_MIN_TEMP":  {"str": "Set min. temp.", "method":self._set_min_temp},
            "SET_EXTRA_TIME":{"str": "Set xtra time",  "method":self._set_extra_time},
            "SET_EXTRA_TEMP":{"str": "Set xtra temp.", "method":self._set_extra_temp},
            "SET_ON_TEMP":   {"str": "Set ON temp.",   "method":self._set_on_temp},
            "SCHEDULE":      {"str": "Config. sched.", "method":self._schedule}
            "DEFAULT":       {"str": "",               "method":self._default}
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

        if TODO pressed(up):
            saved = False
            if TODO long_press():
                current_min = current_min + 2
            else:
                current_min = current_min + 1

        if TODO pressed(down):
            saved = False
            if TODO long_press():
                current_min = current_min - 2
            else:
                current_min = current_min - 1

        if current_min > MAX_TEMP:
            current_min = MAX_TEMP

        if current_min < MIN_TEMP:
            current_min = MIN_TEMP

        if TODO pressed(back):
            self._navigation()

        if TODO pressed(sel):
            saved = True
            set_config({'min_temp':current_min})

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
                ## print special char
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
        if TODO pressed(right):
            self.option_str_method[OPTION_ORDER[effective_pos]]["method"]()

        if TODO pressed(up):
            if cursor_position == 1:
                current_position = (current_position+1)%len(OPTION_ORDER)
            else:
                cursor_position = cursor_position + 1

        if TODO pressed(down):
            if cursor_position == 0:
                current_position = (current_position-1+len(OPTION_ORDER))%len(OPTION_ORDER) # Extra len added for subtractin goblins
            else:
                cursor_position = cursor_position - 1

        if TODO pressed(back):
            self._default()

        self.current_menu = "NAVIGATION"
        self.current_state = {}
        self.current_state["current_position"] = current_position
        self.current_state["cursor_position"] = cursor_position

        return lcd_str

    def generate(self):
        self.option_str_method[current_menu]["method"]()
