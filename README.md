# CO-Project-Final

def A(instruction):
	global output
	output.append("")
	output[-1] += opcode[instruction[0]]
	output[-1] += "00"
	
	for i in range(1,4):
		output[-1] += registers[instruction[i]]

def B(instruction):
	global output
	output.append("")
	if instruction[0] == "mov":
		output[-1] += "00010"
	else:
		output[-1] += opcode[instruction[0]]
	
	output[-1] += "0"

	output[-1] += registers[instruction[1]]
	num = int(instruction[2][1:])
	output[-1] += (7-len(num))*"0" + num
