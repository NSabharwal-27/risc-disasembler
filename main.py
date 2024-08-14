import os

op_type = {
    'add'   :   'r_opType',
    'addi'  :   'i_opType'
}

op_code = {
    'r_opType'    :   0b0110011,
    'i_opType'    :   0b0000011
}

op_funct7 = {
    'add'   :   0x00
}

op_funct3 = {
    'add'   :   0x0
}


#lets begin with opening the .asm file.
asmFile = open('riscv-test.asm', 'r')

for line in asmFile.readlines():
    
    #parsing and cleaning up
    #print(line)                             #let's just print it out to make sure for now
    split_line = line.rstrip().split()       #strip new line characters
    print(split_line)                        #for debug
    
    #op identifier
    opType = op_type.get(split_line[0])
    
    #retrieve opcode funct3 func7
    opCode = op_code.get(opType)
    funct3 = op_funct3.get(split_line[0])
asmFile.close()