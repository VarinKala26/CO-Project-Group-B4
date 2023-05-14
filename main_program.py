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

