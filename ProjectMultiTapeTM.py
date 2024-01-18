class State:
    def __init__(self, name, final=False):
        self.name = name
        self.final = final
        self.next = {}

    def delta(self, symbol):
        pass

    def set_transition(self, input_symbol, write_symbol, next_state, direction):
        pass


class TuringMachine:
    def __init__(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def read_symbol(self):
        pass

    def write_symbol(self, symbol):
        pass

    def transition(self):
        pass

    