class State:
    def __init__(self, name, final=False):
        self.name = name
        self.final = final
        self.next = {}

    #get the symbols from the tapes and the next state
    def delta(self, symbol1, symbol2, symbol3):
        return self.next.get((symbol1, symbol2, symbol3), []) + self.next.get(('', symbol2, symbol3), []) + \
               self.next.get((symbol1, '', symbol3), []) + self.next.get((symbol1, symbol2, ''), []) + \
               self.next.get(('', '', symbol3), []) + self.next.get(('', symbol2, ''), []) + \
               self.next.get((symbol1, '', ''), []) + self.next.get(('','', ''), [])
    
    #transition function that returns the next state, write symbols, and directions based on the input symbols.
    def set_transition(self, input_symbol1, input_symbol2, input_symbol3,
                        write_symbol1, write_symbol2, write_symbol3, 
                        next_state, direction1, direction2, direction3):
        if (input_symbol1, input_symbol2, input_symbol3) not in self.next:
            self.next[(input_symbol1, input_symbol2, input_symbol3)] = []
        #function that sets transitions
        self.next[(input_symbol1, input_symbol2, input_symbol3)].append({
            'next_state': next_state,
            'write_symbol1': write_symbol1,
            'write_symbol2': write_symbol2,
            'write_symbol3': write_symbol3,
            'direction1': direction1,
            'direction2': direction2,
            'direction3': direction3
        })

    #set the state as final
    def set_final(self):
        self.final = True


class MultiTapeTuringMachine:
    def __init__(self, states, symbols, input_string, blank_symbol='B'):
        self.q = states
        self.sigma = symbols #alphabet
        self.blank_symbol = blank_symbol
        self.tape = [blank_symbol] + list(input_string) + [blank_symbol] 
        self.head_position = 1  # Start reading from the first character of the input
        self.current_state = states[0]

    def move_left(self):
        for i in range(len(self.tapes)):
            if self.head_positions[i] > 0:
                self.head_positions[i] -= 1 #move left
            else:
                self.tapes[i].insert(0, self.blank_symbol)

    def move_right(self):
        for i in range(len(self.tapes)):
            self.head_positions[i] += 1 #move right
            if self.head_positions[i] == len(self.tapes[i]):
                self.tapes[i].append(self.blank_symbol)

    def read_symbols(self):
        return self.tape[self.head_position]

    def write_symbols(self, symbol):
        self.tape[self.head_position] = symbol

    def transition(self):
        input_symbols = self.read_symbols()
        transitions = self.current_state.delta(input_symbols)

        if not transitions:
            print(f"No transition for d({self.current_state.name}, {input_symbols})")
            return False

        transition = transitions[0]
        next_state, write_symbols, directions = transition['next_state'], transition['write_symbol'], transition['direction']

        print(f"d({self.current_state.name}, {input_symbols}) = ({next_state.name}, {write_symbols}, {directions})")

        self.current_state = next_state
        self.write_symbols(write_symbols)

        for i in range(len(self.tapes)):
            if directions[i] == 'L':
                self.move_left()
            elif directions[i] == 'R':
                self.move_right()

        self.show_tapes()

        return True


    def show_tapes(self):
        print(f"Tapes at {self.current_state.name}:")
        for i, tape in enumerate(self.tapes):
            print(f"Tape {i + 1}:", end=" ")
            for j, symbol in enumerate(tape):
                if j == self.head_positions[i]:
                    print(f"|_{symbol}_|", end=" ")
                else:
                    print(f"|_{symbol}_|", end=" ")
            print()
        print("\n")

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

    mtm = MultiTapeTuringMachine(states=[q0, q1, q2], symbols=['0', '1'], input_string=["101", "110"])

    while mtm.transition():
        pass

    if mtm.current_state.final:
        print(f"The Strings are Accepted")
    else:
        print(f"The strings are not accepted.")