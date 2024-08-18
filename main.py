import os
import sys
import re
import utils
from lookup_table import registers, op_type, op_code, op_funct7, op_funct3

# Open the assembly file
if not os.path.exists('riscv-test.asm'):
    print("Error: 'riscv-test.asm' file not found.")
    sys.exit(1)

asmFile = open('riscv-test.asm', 'r')

for line in asmFile.readlines():
    line = line.strip()
    if line == '' or line.startswith("#"):
            continue;                       #remove empty lines and comments
    
    #parsing and cleaning up
    #print(line)                             #debug
    line = line.partition('#')[0]
    split_line = re.split(r'[,\s()]+', line)
    
    split_line = [token for token in split_line if token != '']
    print(split_line)                        #for debug
    
    mnemonic = split_line[0]
    opType = op_type.get(split_line[0])
    #print(opType)
    
    if opType is None:
        print(f"Error: Unknown instruction {mnemonic}")
        continue
    
    opCode = op_code.get(opType)
    machinecode = 0
    
    if opType == 'r_opType':
        #format is mnemonic rd, r1, r2
        #also require funct7, funct3
        rd = utils.get_register(split_line[1])
        r1 = utils.get_register(split_line[2])
        r2 = utils.get_register(split_line[3])
        func7 = op_funct7.get(mnemonic)
        func3 = op_funct3.get(mnemonic)
        machinecode = utils.assemble_r_type(opCode, rd, func3, r1, r2, func7)
    
    elif opType == 'i_opType' or opType == 'i_loadType':
        #format is mnmemonic rd, rs1, imm_Value
        #or mnemonic rd, imm(rs1)
        #also require funct3
        rd = utils.get_register(split_line[1])
        func3 = op_funct3.get(mnemonic)
        
        if opType == 'i_opType':
            r1 = utils.get_register(split_line[2])
            imm = utils.parse_immediate(split_line[3])
        else :
            imm = utils.parse_immediate(split_line[2])
            r1 = utils.get_register(split_line[3])
        machinecode = utils.assemble_i_type(opCode, rd, func3, r1, imm)
       
    elif opType == 's_opType':
        #format is mnemonic rd, offset(rs1)
        #also require funct3
        rd = utils.get_register(split_line[1])
        r1 = utils.get_register(split_line[3])
        imm = utils.parse_immediate(split_line[2])
        func3 = op_funct3.get(mnemonic)
        machinecode = utils.assemble_s_type(opCode, imm, func3, rd, r1)
        
    elif opType == 'b_opType':
        #format is mnemonic rs1, rs2, imm
        #also need func3
        rs1 = utils.get_register(split_line[1])
        rs2 = utils.get_register(split_line[2])
        imm = utils.parse_immediate(split_line[3])
        func3 = op_funct3.get(mnemonic)
        machine_code = utils.assemble_b_type(opCode, func3, rs1, rs2, imm)
        
    elif opType == 'u_opType':
        # Format: instr rd, imm
        if len(split_line) != 3:
            print(f"Error: Incorrect number of operands for {mnemonic}")
            continue
        rd = utils.get_register(split_line[1])
        imm = utils.parse_immediate(split_line[2])
        machine_code = utils.assemble_u_type(opCode, rd, imm)
        
    elif opType == 'j_opType':
        # Format: instr rd, imm
        if len(split_line) != 3:
            print(f"Error: Incorrect number of operands for {mnemonic}")
            continue
        rd = utils.get_register(split_line[1])
        imm = utils.parse_immediate(split_line[2])
        machine_code = utils.assemble_j_type(opCode, rd, imm)
    else:
        print(f"Error: Unsupported operation type {opType}")
        continue

    #print(f"{line:<30} => {machine_code:032b} => 0x{machine_code:08x}")
asmFile.close()