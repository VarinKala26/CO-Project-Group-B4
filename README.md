# CO-Project-Final
*********************************************** INTRODUCTION *******************************************************
This project is made by : 
	    	Ritviek Padda:    2022409
            Riya Gupta:       2022410
            Varin Kala:       2022561
            Vimansh Mahajan:  2022572 
			
This document contains information about the Assembler that has been implemented using the code provided in the main file. 
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

5) Finally, an output text file (File name: machinecode.txt) is generated containing the machine code. 

********************************************** ERROR HANDLING ******************************************************

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



