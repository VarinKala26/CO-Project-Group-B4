# CO-Project-Final
*********************************************** INTRODUCTION *******************************************************
This project is made by : 
	    	Ritviek Padda:    2022409
            Riya Gupta:       2022410
            Varin Kala:       2022561
            Vimansh Mahajan:  2022572 
			
This document contains information about the Assembler and simulator that has been implemented using the code provided in the main file. 
Language used to write the program: Python3
********************************************** WORKFLOW- ASSEMBLER **************************************************
1) Assembler first initialises the following: 
	a) Opcode dictionary (opcodes were already provided)
	b) Register-code dictionary (codes for registers were already provided)
	c) File object containing instructions (File name: CO_test.txt)
	d) Length of input file 

2) Assembler then declares the following:
	a) Output list conatining strings resembling lines of machine code
	b) Dictionaries handling addresses of variables and labels used 
	
3) Assembler now loops through the input assembly code, updating the output list and simultaneously checking for errors, if any. (Error handling has been explained below.)

4) Assembler makes suitable changes to the output list by adding addresses of the variables and labels. 

5) Finally, the machine code output is displayed on the terminal. 

********************************************** ERROR HANDLING-ASSEMBLER ******************************************************

The following errors have been taken into account in the code: 
a) Typos in instruction name or register name: "OperationNameError" and "RegisterNameError" 
b) Use of undefined variables: "VariableNotDefinedError"
c) Use of undefined labels: "LabelNotDefinedError"
d) Illegal use of FLAGS register: "FLAGSMisuseError" 
e) Illegal Immediate values (more than 7 bits): "ImmediateValueError"
f) Misuse of labels as variables or vice-versa: "LabelMisuseError" and "VariableMisuseError"
g) Variables not declared at the beginning: "VariableDefinitionError"
h) Missing hlt instruction: "EOFError"
i) hlt not being used as the last instruction: "ImproperEOFError"



Apart from these, we have also considered the following cases as "GeneralSyntaxError":
a) Wrong Syntax: If there are more tokens in instruction than required
b) Immediate Value not starting with "$"

On encountering the above mentioned errors, our assembler notifies the user about the error by not just mentioning the name of the error, but also by mentioning the line number in which the error was encountered.

***************************************************** WORKFLOW-SIMULATOR *****************************************************
1) Our simulator first initialises:
	a) A dictionary named "RF" which contains the names of registers as the key and their respective opcodes as the values. 
	b) A list named "MEM" acting as the program memory. 
	c) A variable for program counter.
	d) A variable acting as halt-flag.

2) The simulator now loops through the input machine code, extracts values stored in the given registers, converts them to integers/floating point and then performs the operation. It checks for overflow where needed, and the final value after the operation is then converted back to binary and suitable changes are made to the registers.

3) After execution of each instruction, the program counter and the value in each register is displayed.

4) At the end of the program, the entire memory (contents of MEM list) is displayed. 
