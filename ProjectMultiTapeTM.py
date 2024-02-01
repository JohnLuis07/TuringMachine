class State:
    def __init__(self, name, final=False):
        self.name = name
        self.final = final
        self.next = {}

    #get the transition from the given symbols
    #retrieve the possible transitions from the current state to the next state based on the input symbols read from the tapes.
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
    def __init__(self, states, symbols, input_string1, input_string2, blank_symbol='B'):
        self.q = states
        self.sigma = symbols #alphabet
        self.blank_symbol = blank_symbol
        # tapes with the input strings at the rightmost end
        self.tape1 = [blank_symbol] + list(input_string1) + [blank_symbol] # [B, 0, 1, 0, 1, B]
        self.tape2 = [blank_symbol] + list(input_string2) + [blank_symbol] # [B, 0, 1, 0, 0, B]
        self.tape3 = [blank_symbol] + [blank_symbol] * (len(input_string2)) + [blank_symbol] # [B, B, B, B, B, B]
        # Set initial head positions
        # algo of tm to leave room for the tape head to move left or right.
        self.head_position1 = len(self.tape1) - 2
        self.head_position2 = len(self.tape2) - 2
        self.head_position3 = len(self.tape3) - 2
        self.current_state = states[0]

    def move_left(self, tape):
        if tape == 1:
            if self.head_position1 > 0:
                self.head_position1 -= 1 # move left
            else:
                self.tape1.insert(0, self.blank_symbol)
        elif tape == 2:
            if self.head_position2 > 0:
                self.head_position2 -= 1 # move left
            else:
                self.tape2.insert(0, self.blank_symbol)
        elif tape == 3:
            if self.head_position3 > 0:
                self.head_position3 -= 1 # move left
            else:
                self.tape3.insert(0, self.blank_symbol)

    def move_right(self, tape):
        if tape == 1:
            self.head_position1 += 1 # move right
            if self.head_position1 == len(self.tape1):
                self.tape1.append(self.blank_symbol)
        elif tape == 2:
            self.head_position2 += 1 # move right
            if self.head_position2 == len(self.tape2):
                self.tape2.append(self.blank_symbol)
        elif tape == 3:
            self.head_position3 += 1 # move right
            if self.head_position3 == len(self.tape3):
                self.tape3.append(self.blank_symbol)

    #It retrieves the symbol from the tape list at the index specified by the head_position attribute.
    def read_symbols(self, tape):
        if tape == 1:
            return self.tape1[self.head_position1]
        elif tape == 2:
            return self.tape2[self.head_position2]
        elif tape == 3:
            return self.tape3[self.head_position3]

    #It sets the value of the tape list at the index specified by the head_position attribute to the given symbol.
    def write_symbols(self, tape, symbol):
        if tape == 1:
            self.tape1[self.head_position1] = symbol
        elif tape == 2:
            self.tape2[self.head_position2] = symbol
        elif tape == 3:
            self.tape3[self.head_position3] = symbol

    def transition(self):
        input_symbol1 = self.read_symbols(1) 
        input_symbol2 = self.read_symbols(2)
        input_symbol3 = self.read_symbols(3)
        transitions = self.current_state.delta(input_symbol1, input_symbol2, input_symbol3) #get the next state, write symbols, and directions

        if not transitions:
            print(f"No transition for d({self.current_state.name}, {input_symbol1}, {input_symbol2}, {input_symbol3})")
            return False

        # access the dictionary
        transition = transitions[0]
        next_state = transition['next_state']
        write_symbol1 = transition['write_symbol1']
        write_symbol2 = transition['write_symbol2']
        write_symbol3 = transition['write_symbol3']
        direction1 = transition['direction1']
        direction2 = transition['direction2']
        direction3 = transition['direction3']

        # print the transition
        print(f"d({self.current_state.name}, {input_symbol1}, {input_symbol2}, {input_symbol3}) = "
              f"({next_state.name}, {write_symbol1}, {write_symbol2}, {write_symbol3}, {direction1}, {direction2}, {direction3})")

        #update the current state, write symbols, and directions
        self.current_state = next_state
        self.write_symbols(1, write_symbol1)
        self.write_symbols(2, write_symbol2)
        self.write_symbols(3, write_symbol3)

        #move the tape head based on the direction
        # tape 1 direction
        if direction1 == 'L':
            self.move_left(1)
        elif direction1 == 'R':
            self.move_right(1)

        # tape 2 direction
        if direction2 == 'L':
            self.move_left(2)
        elif direction2 == 'R':
            self.move_right(2)

        # tape 3 direction
        if direction3 == 'L':
            self.move_left(3)
        elif direction3 == 'R':
            self.move_right(3)

        self.show_tapes()

        return True

    def show_tapes(self):
        print(f"Tapes at {self.current_state.name}:")
        # first tape
        for i, (symbol1, symbol2, symbol3) in enumerate(zip(self.tape1, self.tape2, self.tape3)):
            print(f"|_{symbol1}_|", end=" ")
            if i == self.head_position1:
                print("^", end=" ")
            else:
                print(" ", end=" ")

        print()  # Move to a new line for the second tape
        # second tape
        for i, (symbol1, symbol2, symbol3) in enumerate(zip(self.tape1, self.tape2, self.tape3)):
            print(f"|_{symbol2}_|", end=" ")
            if i == self.head_position2:
                print("^", end=" ")
            else:
                print(" ", end=" ")

        print()  # Move to a new line for the third tape
        # third tape
        for i, (symbol1, symbol2, symbol3) in enumerate(zip(self.tape1, self.tape2, self.tape3)):
            print(f"|_{symbol3}_|", end=" ")
            if i == self.head_position3:
                print("^", end=" ") 
            else:
                print(" ", end=" ")

        print("\n")

#option A
if __name__ == '__main__':
    #define states

    q0 = State('q0')
    q1 = State('q1')
    q2 = State('q2', final=True)

    #L = left, R = right, S = stay
    #define transitions read1, read2, read3, write1, write2, write3, next_state, direction1, direction2, direction3

    # transitions for q0
    q0.set_transition('0', '0', 'B', '0', '0', '0', q0, 'L', 'L', 'L')
    q0.set_transition('B', 'B', 'B', 'B', 'B', '0', q2, 'S', 'S', 'S')
    q0.set_transition('0', '1', 'B', '0', '1', '1', q0, 'L', 'L', 'L')
    q0.set_transition('B', '1', 'B', 'B', '1', '1', q0, 'L', 'L', 'L')
    q0.set_transition('1', '0', 'B', '1', '0', '1', q0, 'L', 'L', 'L')
    q0.set_transition('1', 'B', 'B', '1', 'B', '1', q0, 'L', 'L', 'L')
    q0.set_transition('1', '1', 'B', '1', '1', '0', q1, 'L', 'L', 'L')
    
    # transitions for q1
    q1.set_transition('0', '0', 'B', '0', '0', '1', q0, 'L', 'L', 'L')
    q1.set_transition('B', 'B', 'B', 'B', 'B', '1', q2, 'S', 'S', 'S')
    q1.set_transition('0', '1', 'B', '0', '1', '0', q1, 'L', 'L', 'L')
    q1.set_transition('B', '1', 'B', 'B', '1', '0', q1, 'L', 'L', 'L')
    q1.set_transition('1', '0', 'B', '1', '0', '0', q1, 'L', 'L', 'L')
    q1.set_transition('1', 'B', 'B', '1', 'B', '0', q1, 'L', 'L', 'L')
    q1.set_transition('1', '1', 'B', '1', '1', '1', q1, 'L', 'L', 'L')

    mtm = MultiTapeTuringMachine(states=[q0, q1, q2], symbols=['0', '1'], input_string1="0101", input_string2="0100", blank_symbol='B')

    # print the initial state of the tapes
    while mtm.transition():
        pass

    if mtm.current_state.final:
        print(f"The Strings are Accepted")
    else:
        print(f"The strings are not accepted.")