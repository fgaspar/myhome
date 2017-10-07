from switch import switch

class OnOff(switch.Switch):
    def set_on(self):
        super().set_on()
        ##TODO actually implement this
        print("Switch on")

    def set_off(self):
        super().set_off()
        ##TODO actually implement this
        print("Switch off")

