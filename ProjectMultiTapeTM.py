class State:
    def __init__(self, name, final=False):
        self.name = name
        self.final = final
        self.next = {}

    #get the symbol from the tape list and the next state
    def delta(self, symbol):
        return self.next.get(symbol, []) + self.next.get('', [])
    
    #transition function that returns the next state, write symbol, and direction based on the input symbol.
    def set_transition(self, input_symbol, write_symbol, next_state, direction):
        if input_symbol not in self.next:
            self.next[input_symbol] = []
        #function that sets transitions
        self.next[input_symbol].append({
            'next_state': next_state,
            'write_symbol': write_symbol,
            'direction': direction
        })

    #set the state as final
    def set_final(self):
        self.final = True


class MultiTapeTuringMachine:
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

#option A
if __name__ == '__main__':
    #define states

    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2', final=True)

    #L = left, R = right, S = stay
    #define transitions self, input_symbol, write_symbol, next_state, direction
    q0.set_transition(['0', '0', 'B'], ['0', '0', '0'], q0, ['L', 'L', 'L'])
    q0.set_transition(['B', 'B', 'B'], ['B', 'B', '0'], q2, ['S', 'S', 'S'])
    q0.set_transition(['0', '1', 'B'], ['0', '1', '1'], q0, ['L', 'L', 'L'])
    q0.set_transition(['B', '1', 'B'], ['B', '1', '1'], q0, ['L', 'L', 'L'])
    q0.set_transition(['1', '0', 'B'], ['1', '0', '1'], q0, ['L', 'L', 'L'])
    q0.set_transition(['1', 'B', 'B'], ['1', 'B', '1'], q0, ['L', 'L', 'L'])
    q0.set_transition(['1', '1', 'B'], ['1', '1', '0'], q1, ['L', 'L', 'L'])

    q1.set_transition(['0', '0', 'B'], ['0', '0', '1'], q0, ['L', 'L', 'L'])
    q1.set_transition(['B', 'B', 'B'], ['B', 'B', '1'], q2, ['S', 'S', 'S'])
    q1.set_transition(['0', '1', 'B'], ['0', '1', '0'], q1, ['L', 'L', 'L'])
    q1.set_transition(['B', '1', 'B'], ['B', '1', '0'], q1, ['L', 'L', 'L'])
    q1.set_transition(['1', '0', 'B'], ['1', '0', '0'], q1, ['L', 'L', 'L'])
    q1.set_transition(['1', 'B', 'B'], ['1', 'B', '0'], q1, ['L', 'L', 'L'])
    q1.set_transition(['1', '1', 'B'], ['1', '1', '1'], q1, ['L', 'L', 'L'])