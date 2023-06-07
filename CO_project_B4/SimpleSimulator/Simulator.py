import sys

def ConvertToFloat(binary_string):
    mantissa = binary_string[3:]
    val = 0
    for i in range(5):
        val += (2 ** (-i-1)) * int(mantissa[i])
    
    exponent = ConvertToInt(binary_string[:3])
    val *= 2 ** exponent
    return val

def FloatConvertToBinary(number):
    if number == 0:
        return "0"*16

    exponent = 0
    while number > 1:
        number /= 2
        exponent += 1
    
    binary_string = "0"*8
    exponent_binary = ""
    for i in range(2, -1, -1):
        if 2**i <= exponent:
            exponent_binary += "1"
            exponent -= 2**i
        else:
            exponent_binary += "0"

    binary_string += exponent_binary
    number *= 2**5
    for i in range(4, -1, -1):
        if 2**i <= number:
            binary_string += "1"
            number -= 2**i
        else:
            binary_string += "0"
    
    return binary_string

def DataConvertToBinary(number):
    binary_string = str(bin(number)[2:])
    binary_string = '0'*(16-len(binary_string)) + binary_string
    return binary_string

def PCConvertToBinary(number):
    binary_string = str(bin(number)[2:])
    binary_string = '0'*(7-len(binary_string)) + binary_string
    return binary_string

def ConvertToInt(Binary_string):
    num=0

    if Binary_string[-1] == '\r':
        Binary_string = Binary_string[:-1]
    for i in range(len(Binary_string)):
        if Binary_string[i] == '\r':
            break
        num += 2**((len(Binary_string)-1)-i) * int(Binary_string[i])
    return num

def addition(instruction):
    global RF
    x = instruction
    first = x[7:10]
    second = x[10:13]
    third = x[13:16]

    first_int = str(ConvertToInt(first))
    second_int = str(ConvertToInt(second))
    third_int = str(ConvertToInt(third))

    dest_reg = 'R'+first_int
    source_1 = RF['R'+second_int]
    source_2 = RF['R'+third_int]

    source_1 = ConvertToInt(source_1)
    source_2 = ConvertToInt(source_2)

    res = source_2+source_1
    temp = RF["FLAGS"]

    if res>=2**16:
        RF[dest_reg] = 16*'0'
        RF["FLAGS"] = temp[:12]+'1'+temp[13:]
    else:
        ans = bin(res)
        ans = str(ans)
        ans = ans[2:]
        RF[dest_reg] = '0'*(16-len(ans))+ans
        RF["FLAGS"] = temp[:12]+'0'+temp[13:]

def subtraction(instruction):
    global RF
    a=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    b=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    c=(int(instruction[7])*(2**2))+(int(instruction[8])*(2**1))+(int(instruction[9])*(2**0))
    reg1="R"+str(a)
    reg2="R"+str(b)
    reg3="R"+str(c)

    if ConvertToInt(RF[reg2])-ConvertToInt(RF[reg1])<0:
        RF[reg3]="0"*16
        RF["FLAGS"]=RF["FLAGS"][0:12]+"1"+RF["FLAGS"][13:]
    else:
        RF[reg3]=DataConvertToBinary(ConvertToInt(RF[reg2])-ConvertToInt(RF[reg1]))
        RF["FLAGS"]=RF["FLAGS"][0:12]+"0"+RF["FLAGS"][13:]

def multiply(instruction):
    global RF
    reg1 = str(ConvertToInt(instruction[7:10]))
    reg2 = str(ConvertToInt(instruction[10:13]))
    reg3 = str(ConvertToInt(instruction[13:16]))
    val2 = ConvertToInt(RF["R" + reg2])
    val3 = ConvertToInt(RF["R" + reg3])
    product = val2 * val3

    if product >= 2**16:
        RF["R" + reg1] = "0000000000000000"
        RF["FLAGS"] = RF["FLAGS"][:-4] + "1" + RF["FLAGS"][-3:]
    else:
        RF["R" + reg1] = DataConvertToBinary(product)
        RF["FLAGS"] = RF["FLAGS"][:-4] + "0" + RF["FLAGS"][-3:]

def moveImmediate(instruction):
    global RF
    reg = str(ConvertToInt(instruction[6:9]))
    location = ConvertToInt(instruction[9:16])
    val_binary = MEM[location]
    RF["R" + reg] = val_binary

def moveRegister(instruction):
    first_reg = 'R' + str(ConvertToInt(instruction[10:13]))
    second_reg = 'R' + str(ConvertToInt(instruction[13:16]))
    if second_reg == "R7":
        second_reg = "FLAGS"
    RF[first_reg] = RF[second_reg]

def load(instruction):
    moveImmediate(instruction)

def store(instruction):
    global MEM
    reg = str(ConvertToInt(instruction[6:9]))
    location = ConvertToInt(instruction[9:16])
    MEM[location] = RF["R" + reg]

def divide(instruction):
    global RF
    a= (int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    b= ((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    reg3= "R"+str(a)
    reg4= "R"+ str(b)
    if RF[reg4]=="0"*16:
        RF["FLAGS"]=RF["FLAGS"][0:12]+"1"+RF["FLAGS"][13:]
        RF["R0"]="0"*16
        RF["R1"]="0"*16
    else:
        RF["R0"]=DataConvertToBinary((ConvertToInt(RF[reg3]))//(ConvertToInt(RF[reg4])))
        RF["R1"]= DataConvertToBinary((ConvertToInt(RF[reg3]))%(ConvertToInt(RF[reg4])))
        RF["FLAGS"]=RF["FLAGS"][0:12]+"0"+RF["FLAGS"][13:]

def rightShift(instruction):
    global RF
    reg = str(ConvertToInt(instruction[6:9]))
    reg = "R" + reg
    val = ConvertToInt(instruction[9:16])
    if val > 16:
        RF[reg] = "0"*16
    RF[reg] = "0" * val + RF[reg][:-val]

def leftShift(instruction):
    global RF
    reg = str(ConvertToInt(instruction[6:9]))
    reg = "R" + reg
    val = ConvertToInt(instruction[9:])
    if val > 16:
        RF[reg] = "0"*16
    RF[reg] = RF[reg][val:] + "0" * val

def xor(instruction):
    global RF
    a=(int(instruction[7])*(2**2))+(int(instruction[8])*(2**1))+(int(instruction[9])*(2**0))
    b=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    c=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    reg1= "R"+str(a)
    reg2= "R"+str(b)
    reg3= "R"+str(c)
    RF[reg1]=DataConvertToBinary((ConvertToInt(RF[reg2]))^(ConvertToInt(RF[reg3])))

def bitwiseOr(instruction):
    global RF
    a=(int(instruction[7])*(2**2))+(int(instruction[8])*(2**1))+(int(instruction[9])(2**0))
    b=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])(2**0))
    c=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    reg1= "R"+str(a)
    reg2= "R"+str(b)
    reg3= "R"+str(c)
    RF[reg1]=DataConvertToBinary((ConvertToInt(RF[reg2])) | (ConvertToInt(RF[reg3])))

def bitwiseAnd(instruction):
    global RF
    a=(int(instruction[7])*(2**2))+(int(instruction[8])*(2**1))+(int(instruction[9])*(2**0))
    b=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    c=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    reg1= "R"+str(a)
    reg2= "R"+str(b)
    reg3= "R"+str(c)
    RF[reg1]=DataConvertToBinary((ConvertToInt(RF[reg2])) & (ConvertToInt(RF[reg3])))

def invert(instruction):
    global RF
    a=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    b=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    reg1= "R"+str(a)
    reg2= "R"+str(b)
    RF[reg1]=DataConvertToBinary((ConvertToInt(RF[reg2]))^((2**16)-1))

def compare(instruction):
    global RF
    a=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    b=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    reg1= "R"+str(a)
    reg2= "R"+str(b)
    if ConvertToInt(RF[reg1])<ConvertToInt(RF[reg2]):
        RF["FLAGS"]=RF["FLAGS"][0:13]+"100"
    elif ConvertToInt(RF[reg1])>ConvertToInt(RF[reg2]):
        RF["FLAGS"]=RF["FLAGS"][0:13]+"010"
    elif ConvertToInt(RF[reg1])==ConvertToInt(RF[reg2]):
        RF["FLAGS"]=RF["FLAGS"][0:13]+"001"

def uncondJump(instruction):
    return ConvertToInt(instruction[9:])

def f_addition(instruction):
    global RF
    x = instruction
    first = x[7:10]
    second = x[10:13]
    third = x[13:16]

    first_int = str(ConvertToInt(first))
    second_int = str(ConvertToInt(second))
    third_int = str(ConvertToInt(third))

    dest_reg = 'R'+first_int
    source_1 = RF['R'+second_int]
    source_2 = RF['R'+third_int]

    source_1 = ConvertToFloat(source_1[8:16])
    source_2 = ConvertToFloat(source_2[8:16])

    res = source_2+source_1
    temp = RF["FLAGS"]
    
    if res>=124:
        RF[dest_reg] = 16*'0'
        RF["FLAGS"] = temp[:12]+'1'+temp[13:]
    else:
        RF[dest_reg] = FloatConvertToBinary(res)
        RF["FLAGS"] = temp[:12]+'0'+temp[13:]

def f_subtraction(instruction):
    global RF
    a=((int(instruction[13]))*(2**2))+(int(instruction[14])*(2**1))+(int(instruction[15])*(2**0))
    b=(int(instruction[10])*(2**2))+(int(instruction[11])*(2**1))+(int(instruction[12])*(2**0))
    c=(int(instruction[7])*(2**2))+(int(instruction[8])*(2**1))+(int(instruction[9])*(2**0))
    reg1="R"+str(a)
    reg2="R"+str(b)
    reg3="R"+str(c)

    val = ConvertToFloat(RF[reg2][8:16])-ConvertToFloat(RF[reg1][8:16])
    if val < 0:
        RF[reg3]="0"*16
        RF["FLAGS"]=RF["FLAGS"][0:12]+"1"+RF["FLAGS"][13:]
    else:
        RF[reg3]=FloatConvertToBinary(val)
        RF["FLAGS"]=RF["FLAGS"][0:12]+"0"+RF["FLAGS"][13:]

def moveFImmediate(instruction):
    global RF
    reg = "R" + str(ConvertToInt(instruction[5:8]))
    RF[reg] = "00000000" + instruction[8:]

def jumpLessThan(instruction):
    if RF["FLAGS"][-3] == '1':
        return ConvertToInt(instruction[9:16])
    
    return new_PC

def jumpGreaterThan(instruction):
    if RF["FLAGS"][-2] == '1':
        return ConvertToInt(instruction[9:16])
    
    return new_PC

def jumpEqual(instruction):
    if RF["FLAGS"][-1] == '1':
        return ConvertToInt(instruction[9:16])
    
    return new_PC

def execute(instruction, PC):
    halted, new_PC = False, PC + 1
    opcode = instruction[:5]
    if opcode == "00000":
        addition(instruction)
    elif opcode == "00001":
        subtraction(instruction)
    elif opcode == "00010":
        moveImmediate(instruction)
    elif opcode == "00011":
        moveRegister(instruction)
    elif opcode == "00100":
        load(instruction)
    elif opcode == "00101":
        store(instruction)
    elif opcode == "00110":
        multiply(instruction)
    elif opcode == "00111":
        divide(instruction)
    elif opcode == "01000":
        rightShift(instruction)
    elif opcode == "01001":
        leftShift(instruction)
    elif opcode == "01010":
        xor(instruction)
    elif opcode == "01011":
        bitwiseOr(instruction)
    elif opcode == "01100":
        bitwiseAnd(instruction)
    elif opcode == "01101":
        invert(instruction)
    elif opcode == "01110":
        compare(instruction)
    elif opcode == "01111":
        new_PC = uncondJump(instruction)
    elif opcode == "10000":
        f_addition(instruction)
    elif opcode == "10001":
        f_subtraction(instruction)
    elif opcode == "10010":
        moveFImmediate(instruction)
    elif opcode == "11100":
        new_PC = jumpLessThan(instruction)
    elif opcode == "11101":
        new_PC = jumpGreaterThan(instruction)
    elif opcode == "11111":
        new_PC = jumpEqual(instruction)
    elif opcode == "11010":
        halted = True
    
    return halted, new_PC

MEM = []
for i in range(256):
    MEM.append("0000000000000000")

variable_location = 0

for inp in sys.stdin:
    MEM[variable_location] = inp
    variable_location += 1

PC = 0
halted = False

RF = {"R0": "0000000000000000", "R1": "0000000000000000", "R2": "0000000000000000", "R3": "0000000000000000", \
      "R4": "0000000000000000", "R5": "0000000000000000", "R6": "0000000000000000", "FLAGS": "0000000000000000"}

while not halted:
    instruction = MEM[PC]
    if instruction[-1] == "\r":
        instruction = instruction[:-1]
    halted, new_PC = execute(instruction, PC)
    sys.stdout.write(PCConvertToBinary(PC) + ' '*8)
    for reg in RF:
        sys.stdout.write(RF[reg] + ' ')
    sys.stdout.write('\n')
    PC = new_PC

for i in range(128):
    sys.stdout.write(MEM[i] + '\n')
