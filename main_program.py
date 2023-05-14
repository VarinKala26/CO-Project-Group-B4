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
