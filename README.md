# TuringMachine

NOTE: JUST CHANGE THE TRANSITION FUNCTION according to what do you want to happen to each of the turing machine in the main driver.

Code content:
1. Deterministic Turing Machine - produce one output.
-DEFAULT TRANSITION FUNCTION: 2'S COMPLEMENT

2. Nondeterministic Turing Machine - produce multiple outputs based on the transition function.
-DEFAULT TRANSITION FUNCTION: 2'S COMPLEMENT WITH MULTIPLE OUTPUTS

3. Deterministic Multitape Turing Machine - produce multiple tapes and output. 

- 3 tapes
	- first tape has the first input (in binary), tape head points to the rightmost input symbol
	- second tape has the second input (in binary), tape head points to the rightmost input symbol
	- third tape contains all "B", tape head points somewhere at the right
	- all three tape heads are pointing on the same column