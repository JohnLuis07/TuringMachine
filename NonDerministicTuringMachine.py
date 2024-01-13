# Define a State class representing a state in the Turing Machine
class State:
    def __init__(self, name, final=False):
        # Initialize the state with a name, and a flag indicating if it's a final state
        self.name = name
        self.final = final
        # Use a dictionary to store transitions based on input symbols
        self.next = {}

    def delta(self, symbol):
        # Get transitions for the given symbol or epsilon ('') if no specific transition
        return self.next.get(symbol, []) + self.next.get('', [])

    def set_transition(self, input_symbol, write_symbol, next_state, direction):
        # Set a transition for the state
        if input_symbol not in self.next:
            self.next[input_symbol] = []
        self.next[input_symbol].append({
            'next_state': next_state,
            'write_symbol': write_symbol,
            'direction': direction
        })

    def set_final(self):
        # Set the state as a final state
        self.final = True


# Define a TuringMachine class representing a Turing Machine
class TuringMachine:
    def __init__(self, states, symbols, input_string, blank_symbol='B'):
        # Initialize the Turing Machine with states, symbols, input string, and a blank symbol
        self.q = states
        self.sigma = symbols
        self.blank_symbol = blank_symbol
        # Initialize the tape with the input string surrounded by blank symbols
        self.tape = [blank_symbol] + list(input_string) + [blank_symbol]
        # Initialize the head position to start reading from the first character of the input
        self.head_position = 1
        # Initialize the current state to the initial state
        self.current_state = states[0]
        # List to store final tape configurations
        self.final_tapes = []

    def move_left(self):
        # Move the tape head to the left
        if self.head_position > 0:
            self.head_position -= 1
        else:
            # If already at the leftmost end, insert a blank symbol to the left
            self.tape.insert(0, self.blank_symbol)

    def move_right(self):
        # Move the tape head to the right
        self.head_position += 1
        # If at the rightmost end, append a blank symbol to the right
        if self.head_position == len(self.tape):
            self.tape.append(self.blank_symbol)

    def read_symbol(self):
        # Read the symbol under the tape head
        return self.tape[self.head_position]

    def write_symbol(self, symbol):
        # Write a symbol to the current position on the tape
        self.tape[self.head_position] = symbol

    def transition(self):
        # Execute a transition based on the current state and symbol under the tape head
        input_symbol = self.read_symbol()
        transitions = self.current_state.delta(input_symbol)

        # If no transitions are available, print a message and return False
        if not transitions:
            print(f"No transition for d({self.current_state.name}, {input_symbol})")
            return False

        # List to store new tapes
        new_tapes = []

        # Iterate over possible transitions
        for transition in transitions:
            next_state, write_symbol, direction = transition['next_state'], transition['write_symbol'], transition['direction'] #Unpack the information from the transition dictionary.

            # Print the transition information
            print(f"d({self.current_state.name}, {input_symbol}) = ({next_state.name}, {write_symbol}, {direction})")   # Print information about the transition, indicating the source state, input symbol, and the next state, symbol to be written, and direction.

            # Create a copy of the Turing machine
            tm_copy = self.copy()       #Create a copy of the current Turing machine using the copy method.
            tm_copy.current_state = next_state #Update the copy's current state based on the transition.
            tm_copy.write_symbol(write_symbol) #Write the symbol to the tape head position of the copy.

            # Move the tape head based on the direction
            if direction == 'L':
                tm_copy.move_left()
            elif direction == 'R':
                tm_copy.move_right()

            # Show the tape configuration
            tm_copy.show_tape()

            # Add the new Turing machine to the list
            new_tapes.append(tm_copy)

        # If multiple transitions are possible, print information about the new tapes
        if len(new_tapes) > 1:      #Check if there are multiple possible transitions
            print("Creating new tapes:")
            for i, new_tm in enumerate(new_tapes):      # Print a message indicating that multiple tapes are being created.
                print(f"Tape {i + 1}: {''.join(new_tm.tape[1:-1])}")    #Print the index and the content of each new tape (excluding the leading and trailing blank symbols).

        # Update the original Turing Machine with the configuration from the first tape in new_tapes
        self.tape = new_tapes[0].tape
        self.head_position = new_tapes[0].head_position
        self.current_state = new_tapes[0].current_state

        # If the current state is final, append the final tape configuration
        if self.current_state.final:
            self.final_tapes.append(''.join(self.tape[1:-1]))   #If it is, append the final tape configuration (excluding leading and trailing blank symbols) to the list of final tapes.

        # Return True to indicate successful transition
        return True

    def show_tape(self):
        # Display the current tape configuration
        print(f"Tape at {self.current_state.name}:", end=" ")
        for i, symbol in enumerate(self.tape):
            if i == self.head_position:
                print(f"|_{symbol}_|", end=" ")
            else:
                print(f"|_{symbol}_|", end=" ")
        print("\n")

    def copy(self):
        # Create a copy of the Turing machine with the same configuration
        tm_copy = TuringMachine(states=self.q, symbols=self.sigma, input_string="", blank_symbol=self.blank_symbol) #create a new instance of the TuringMachine class (tm_copy) with the same set of states, symbols, and blank symbol. The input_string is initialized as an empty string.
        tm_copy.tape = self.tape.copy() #Copy the tape configuration of the current Turing machine to the tm_copy. This ensures that the content of the tape is the same, but they are independent objects
        tm_copy.head_position = self.head_position  #Copy the head position of the current Turing machine to tm_copy.
        tm_copy.current_state = self.current_state
        tm_copy.final_tapes = self.final_tapes.copy()   #Copy the list of final tapes from the current Turing machine to tm_copy. This ensures that modifications to final_tapes in one Turing machine don't affect the other.
        return tm_copy  #Return turing machine copy


# Example Usage
if __name__ == "__main__":
    # Define two states q0 and q1
    q0 = State("q0")
    q1 = State("q1")



    # Set transitions for state q0
    q0.set_transition('0', '1', q0, 'R')
    q0.set_transition('1', '0', q0, 'R')
    q0.set_transition('1', '1', q1, 'R')

    # Set a transition for state q1
    q1.set_transition('0', '0', q1, 'R')

    # Create a Turing Machine with states q0 and q1, symbols 0 and 1, input string "101", and blank symbol 'B'
    tm = TuringMachine(states=[q0, q1], symbols=['0', '1'], input_string="101", blank_symbol='B')

    # Process the input string by repeatedly calling the transition method until no more transitions are possible
    while tm.transition():
        pass

    # If final tapes are not empty, the input string is accepted, and final tape configurations are printed
    if tm.final_tapes:
        print("The String is Accepted. Final tapes:")
        for final_tape in tm.final_tapes:
            print(final_tape)
    else:
        print(f"The string is not accepted.")