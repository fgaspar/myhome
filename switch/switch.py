class Switch(object):
    def __init__(self, attr = None):
        self.state = 0
        self.grad = 0.0
        if attr:
            if isinstance(attr, dict):
                self.attr = attr
            else:
                raise RuntimeError('Unexpected type for attr, should be dict')
        else:
            self.attr = dict()

    def set_on(self):
        self.state = 1

    def set_off(self):
        self.state = 0

    def get_state(self):
        return (self.state)

    def get_grad(self):
        return (self.grad)

    def set_grad(self, grad):
        self.grad = float(grad)

    def __str__(self):
        print ('Current state: {} , {}%'.format({0:'OFF', 1:'ON'}[self.state], self.grad*100.0))