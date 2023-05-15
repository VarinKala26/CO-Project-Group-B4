# Final code
'''
GeneralSyntaxError:
    Wrong Syntax: If there are more tokens in instruction than required
    Immediate Value must start with $
'''

opcode = {"add": "00000", "sub": "00001", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111", \
          "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101", "cmp": "01110", \
          "jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111", "addf": "10000", "subf": "10001", "movf": "10010"}
          # 'mov', and 'hlt' not included

registers = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

output = []
variable_rec = {}
variable_call = {}
label_call = {}
label_pos = {}

program_counter = 0

def A(instruction, output, program_counter):
    global error_flag

    output.append(opcode[instruction[0]] + "00")

    for i in range(1, 4):
        if instruction[i] == "FLAGS":
            print("FLAGSMisuseError: Register FLAGS cannot be used for operation \'", instruction[0], "\'! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            return
        
        if instruction[i] not in registers:
            print("RegisterNameError: Register \'", instruction[i], "\' does not exist! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            return
        
        output[program_counter] += registers[instruction[i]]
    
    try:
        check = instruction[4]
    except:
        print("GeneralSyntaxError: Wrong Syntax! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1


def B(instruction, output, program_counter):
    global error_flag

    output.append("")
    if instruction[0] == "mov":
        output[program_counter] += "00010"
    else:
        output[program_counter] += opcode[instruction[0]]

    if instruction[0] != "movf":
        output[program_counter] += "0"

    if instruction[1] == "FLAGS":
        print("FLAGSMisuseError: Register FLAGS cannot be used for operation \'", instruction[0], "\'! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
        return
    
    if instruction[1] not in registers:
        print("RegisterNameError: Register \'", instruction[1], "\' does not exist! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
        return

    output[program_counter] += registers[instruction[1]]

    if instruction[0] != "movf":
        if instruction[2][0] != "$":
            print("GeneralSyntaxError: Immediate Value must start with \'$\'! (Line ", program_counter + variable_count + 1, ")", sep = '')

        if '.' in instruction[2][1:] or int(instruction[2][1:]) < 0 or int(instruction[2][1:]) > 127:
            print("ImmediateValueError: Value cannot be evaluated! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            return

        num = bin(int(instruction[2][1:]))
        num = num[2:]
        output[program_counter] += (7 - len(num)) * "0" + num
    else:
        #Part of Q3
        pass
    
    try:
        check = instruction[3]
    except:
        print("GeneralSyntaxError: Wrong Syntax! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
        
def C(instruction, output, program_counter):
    global error_flag

    if instruction[0] == "mov":
        output.append("0001100000")
    else:
        output.append(opcode[instruction[0]] + "00000")

    for i in range(1, 3):
        if instruction[0] != "mov" and instruction[i] == "FLAGS":
            print("FLAGSMisuseError: Register FLAGS cannot be used for operation \'", instruction[0], "\'! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            return
        
        if instruction[i] not in registers:
            print("RegisterNameError: Register \'", instruction[i], "\' does not exist! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            return
        
        output[program_counter] += registers[instruction[i]]
    
    try:
        check = instruction[3]
    except:
        print("GeneralSyntaxError: Wrong Syntax! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1

def D(instruction, output, variable_call, program_counter):
    global error_flag
    
    if instruction[1] == "FLAGS":
        print("FLAGSMisuseError: Register FLAGS cannot be used for operation \'", instruction[0], "\'! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
        return
    
    if instruction[1] not in registers:
        print("RegisterNameError: Register \'", instruction[1], "\' does not exist! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
        return

    output.append(opcode[instruction[0]] + "0" + registers[instruction[1]])
    
    variable_call[program_counter] = instruction[2]

    try:
        check = instruction[3]
    except:
        print("GeneralSyntaxError: Wrong Syntax! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1

def E(instruction, output, label_call, program_counter):
    global error_flag

    output.append(opcode[instruction[0]] + "0000")
    label_call[program_counter] = instruction[1]

    try:
        check = instruction[4]
    except:
        print("GeneralSyntaxError: Wrong Syntax! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
		
error_flag = 0
hlt_flag = 0
variable_count = 0

f = open("CO_test.txt")
input_length = len(f.readlines())
f.close()

f = open("CO_test.txt")
while True:
    if error_flag:
        break

    instruction = f.readline().split()

    if instruction == []:
        if program_counter + variable_count == input_length:
            if hlt_flag == 0:
                print("EOFError: Missing \'hlt\' instruction!")
                error_flag = 1
            break
        continue

    if hlt_flag:
        print("ImproperEOFError: \'hlt\' not being used as last instruction!")
        error_flag = 1
        break


    if instruction[0][-1] == ':':
        label_pos[instruction[0][:-1]] = program_counter
        instruction = instruction[1:]

    if instruction[0] == "var":
        if program_counter != 0:
            print("VariableDefinitionError: Variable must be declared at the beginning! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            break
        variable_rec[instruction[1]] = -1;
        variable_count += 1
        continue

	if instruction[0] in ["add", "sub", "mul", "xor", "or", "and", "addf", "subf"]:
        A(instruction, output, program_counter)
    elif instruction[0] in ["rs", "ls", "movf"] or (instruction[0] == "mov" and instruction[2] not in registers):
        B(instruction, output, program_counter)
    elif instruction[0] in ["mov", "div", "not", "cmp"]:
        C(instruction, output, program_counter)
    elif instruction[0] in ["ld", "st"]:
        D(instruction, output, variable_call, program_counter)
    elif instruction[0] in ["jmp", "jlt", "jgt", "je"]:
        E(instruction, output, label_call, program_counter)
    elif instruction[0] == "hlt":
        try:
            check = instruction[1]
        except:
            print("GeneralSyntaxError: Wrong Syntax! (Line ", program_counter + variable_count + 1, ")", sep = '')
            error_flag = 1
            break

        output.append("11010" + 11 * "0")
        hlt_flag = 1
    else:
        print("OperationNameError: Operation \'", instruction[0], "\' is incorrect! (Line ", program_counter + variable_count + 1, ")", sep = '')
        error_flag = 1
	
	program_counter += 1

f.close()

if error_flag == 0:
    for i in variable_rec:
        program_counter += 1
        variable_rec[i] = program_counter

    for i in variable_call:
        if variable_call[i] not in variable_rec:
            if variable_call[i] in label_pos:
                print("LabelMisuseError: Label \'", variable_call[i], "\' has been called as Variable! (Line ", i + variable_count + 1, ")", sep = '')
            else:
                print("VariableNotDefinedError: Label \'", variable_call[i], "\' has not been defined! (Line ", i + variable_count + 1, ")", sep = '')
            error_flag = 1
            break

        num = bin(variable_rec[variable_call[i]])[2:]
        output[i] += (7 - len(num)) * "0" + num

    for i in label_call:
        if error_flag == 1:
            break

        if label_call[i] not in label_pos:
            if label_call[i] in variable_rec:
                print("VariableMisuseError: Variable \'", label_call[i], "\' has been called as Label! (Line ", i + variable_count + 1, ")", sep = '')
            else:
                print("LabelNotDefinedError: Label \'", label_call[i], "\' has not been defined! (Line ", i + variable_count + 1, ")", sep = '')
            error_flag = 1
            break
        
        num = bin(label_pos[label_call[i]])[2:]
        output[i] += (7 - len(num)) * "0" + num

    if error_flag == 0:
        f = open("machinecode.txt", "w")
        f.write("\n".join(output))
        f.close()
