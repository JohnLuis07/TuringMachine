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


class TuringMachine:
    def __init__(self, states, symbols, input_string, blank_symbol='B'):
        self.q = states
        self.sigma = symbols #alphabet
        self.blank_symbol = blank_symbol
        self.tape = [blank_symbol] + list(input_string) + [blank_symbol] 
        self.head_position = 1  # Start reading from the first character of the input
        self.current_state = states[0]

    #manipulate the tape and head position.
        
    #function that move left in the tape
    def move_left(self):
        if self.head_position > 0:
            self.head_position -= 1
        else:
            self.tape.insert(0, self.blank_symbol)

    #function that move right in the tape
    def move_right(self):
        self.head_position += 1
        if self.head_position == len(self.tape):
            self.tape.append(self.blank_symbol)

    #It retrieves the symbol from the tape list at the index specified by the head_position attribute.
    def read_symbol(self):
        return self.tape[self.head_position]

    #It sets the value of the tape list at the index specified by the head_position attribute to the given symbol.
    def write_symbol(self, symbol):
        self.tape[self.head_position] = symbol

    
    def transition(self):
        input_symbol = self.read_symbol()
        transitions = self.current_state.delta(input_symbol) ##responsible for returning the set of transitions based on the input symbol.

        #if no next transition in from input symbol
        if not transitions:
            print(f"No transition for d({self.current_state.name}, {input_symbol})")
            return False

        transition = transitions[0]
        #get the value in the dictionary
        next_state, write_symbol, direction = transition['next_state'], transition['write_symbol'], transition['direction']

        #display the transition function
        print(f"d({self.current_state.name}, {input_symbol}) = ({next_state.name}, {write_symbol}, {direction})")

        self.current_state = next_state
        self.write_symbol(write_symbol)

        #manipulate the direction of the tape either left or right
        if direction == 'L':
            self.move_left()
        elif direction == 'R':
            self.move_right()

        #prints the tape
        self.show_tape()

        return True

    #function to display the tape
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
    q3 = State("q3")
 

    # Set Transitions (read, write, move)
    q0.set_transition('0', '0', q0, 'R')  # From q0, read 0, write 0, move right, stay in q0
    q0.set_transition('1', '1', q0, 'R')  # From q0, read 1, write 1, move right, stay in q0
    q0.set_transition('B', 'B', q1, 'L')  # From q0, read blank, write blank, move left, go to q1

    # Set Transitions for q1 to move left and subtract 1 for each 0 until reaching the beginning
    q1.set_transition('0', '0', q1, 'L')  # From q1, read 0, write 0, move left, stay in q1
    q1.set_transition('1', '1', q3, 'L')  # From q1, read 1, write 1, move left, stay in q1
    q1.set_transition('B', 'B', q1, 'L')  # From q0, read blank, write blank, move left, go to q1

    

    q3.set_transition('0', '1', q3, 'L')  # From q1, read blank, write blank, move right, go to q2
    q3.set_transition('1', '0', q3, 'L')  # From q1, read 0, write blank, stay in q1 (subtract 1)
    q3.set_transition('B', 'B', q2, 'S')  # From q1, read 0, write blank, stay in q1 (subtract 1)
    
    
    # Create Turing Machine
    tm = TuringMachine(states=[q0, q1, q2], symbols=['0', '1'], input_string="101", blank_symbol='B')

    # Process the input string
    while tm.transition():
        pass

    if tm.current_state.final:
        print(f"The String is Accepted --- The result after subtracting 1 based on the number of zeros is: {''.join(tm.tape[1:-1])}")
    else:
        print(f"The string is not accepted.")