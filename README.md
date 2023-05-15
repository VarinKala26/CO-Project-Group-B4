# CO-Project-Final
****************************************ASSEMBLER**************************************************************
This project is made by : 
	    	Ritviek Padda:    2022409
            Riya Gupta:       2022410
            Varin Kala:       2022561
            Vimansh Mahajan:  2022572 
			
This document contains information about the Assembler that has been implemented using the code provided in the main file.        
****************************************WORKFLOW********************************************************************


****************************************ERROR HANDLING **************************************************************

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



