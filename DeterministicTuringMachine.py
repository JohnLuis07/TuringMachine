class State:
    def __init__(self, name, final=False):
        self.name = name
        self.final = final
        self.next = {}

    def delta(self, symbol):
        transitions_for_symbol = self.next.get(symbol, [])
        transitions_for_empty = self.next.get('', [])
        return transitions_for_symbol + transitions_for_empty

    def set_transition(self, input_symbol, write_symbol, next_state, direction):
        if input_symbol not in self.next:
            self.next[input_symbol] = []
        self.next[input_symbol].append({
            'next_state': next_state,
            'write_symbol': write_symbol,
            'direction': direction
        })

    def set_final(self):
        self.final = True


class TM:
    def __init__(self, states, symbols, blank_symbol='B'):
        self.q = states
        self.sigma = symbols
        self.blank_symbol = blank_symbol
        self.tape = ['B']
        self.head_position = 0
        self.current_state = states[0]

    def move_left(self):
        if self.head_position > 0:
            self.head_position -= 1
        else:
            self.tape.insert(0, self.blank_symbol)

    def move_right(self):
        self.head_position += 1
        if self.head_position == len(self.tape):
            self.tape.append(self.blank_symbol)

    def read_symbol(self):
        return self.tape[self.head_position]

    def write_symbol(self, symbol):
        self.tape[self.head_position] = symbol

    def transition(self, input_symbol):
        transitions = self.current_state.delta(input_symbol)

        if not transitions:
            print(f"No transition for d({self.current_state.name}, {input_symbol})")
            return False

        transition = transitions[0]
        next_state, write_symbol, direction = transition['next_state'], transition['write_symbol'], transition['direction']

        print(f"d({self.current_state.name}, {input_symbol}) = ({next_state.name}, {write_symbol}, {direction})")

        self.current_state = next_state
        self.write_symbol(write_symbol)

        if direction == 'L':
            self.move_left()
        elif direction == 'R':
            self.move_right()

        self.show_tape()

        return True

    def show_tape(self):
        print(f"Tape at {self.current_state.name}:", end=" ")
        for i, symbol in enumerate(self.tape):
            if i == self.head_position:
                print(f"|_{symbol}_|", end=" ")
            else:
                print(f"|_{symbol}_|", end=" ")
        print("\n")


# Example Usage
if __name__ == "__main__":
    # Define States
    q0 = State("q0")
    q1 = State("q1")
    q2 = State("q2", final=True)

    # Set Transitions (read, write, move)
    q0.set_transition('0', '1', q0, 'R')  # From q0, read 0, write 1, move right, stay in q0
    q0.set_transition('1', '0', q0, 'R')  # From q0, read 1, write 0, move right, stay in q0
    q0.set_transition('B', 'B', q1, 'L')  # From q0, read blank, write blank, move left, go to q1

    # Set Transitions for q1 to move left and rewrite symbols until reaching the beginning
    q1.set_transition('0', '0', q1, 'L')  # From q1, read 0, write 0, move left, stay in q1
    q1.set_transition('1', '1', q1, 'L')  # From q1, read 1, write 1, move left, stay in q1
    q1.set_transition('B', 'B', q2, 'R')  # From q1, read blank, write blank, move right, go to q2

    # Create Turing Machine
    tm = TM(states=[q0, q1, q2], symbols=['0', '1'], blank_symbol='B')

    # Input String
    print("This Turing Machine reverses a string of 0s and 1s.")
    test_string = input("Enter a binary string (e.g., '10'): ")
    print()

    # Process the input string
    for symbol in test_string:
        tm.transition(symbol)

    # Finish processing by reading a blank symbol
    tm.transition('B')

    if tm.current_state.final:
        print(f"The reversed string is: {''.join(reversed(test_string))}")
        print(f"The original string was: {test_string}")
        print(f"The Turing Machine has reversed the input.")
    else:
        print(f"The string '{test_string}' is not accepted.")





