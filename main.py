import os
import sys
import re

# Dictionaries for instruction formats
op_type = {
    'add':      'r_opType',
    'sub':      'r_opType',
    'sll':      'r_opType',
    'slt':      'r_opType',
    'sltu':     'r_opType',
    'xor':      'r_opType',
    'srl':      'r_opType',
    'sra':      'r_opType',
    'or':       'r_opType',
    'and':      'r_opType',
    'addi':     'i_opType',
    'slti':     'i_opType',
    'sltiu':    'i_opType',
    'xori':     'i_opType',
    'ori':      'i_opType',
    'andi':     'i_opType',
    'slli':     'i_shiftType',
    'srli':     'i_shiftType',
    'srai':     'i_shiftType',
    'lb':       'i_loadType',
    'lh':       'i_loadType',
    'lw':       'i_loadType',
    'lbu':      'i_loadType',
    'lhu':      'i_loadType',
    'sb':       's_opType',
    'sh':       's_opType',
    'sw':       's_opType',
    'beq':      'b_opType',
    'bne':      'b_opType',
    'blt':      'b_opType',
    'bge':      'b_opType',
    'bltu':     'b_opType',
    'bgeu':     'b_opType',
    'lui':      'u_opType',
    'auipc':    'u_opType',
    'jal':      'j_opType',
    'jalr':     'i_opType',
    # Add more instructions as needed
}

op_code = {
    'r_opType':     0b0110011,
    'i_opType':     0b0010011,
    'i_loadType':   0b0000011,
    'i_shiftType':  0b0010011,
    's_opType':     0b0100011,
    'b_opType':     0b1100011,
    'u_opType':     0b0110111,
    'j_opType':     0b1101111,
    # Add more opcodes as needed
}

op_funct7 = {
    'add':          0x00,
    'sub':          0x20,
    'sll':          0x00,
    'slt':          0x00,
    'sltu':         0x00,
    'xor':          0x00,
    'srl':          0x00,
    'sra':          0x20,
    'or':           0x00,
    'and':          0x00,
    'slli':         0x00,
    'srli':         0x00,
    'srai':         0x20,
    # Add more funct7 as needed
}

op_funct3 = {
    'add': 0x0,
    'sub': 0x0,
    'sll': 0x1,
    'slt': 0x2,
    'sltu': 0x3,
    'xor': 0x4,
    'srl': 0x5,
    'sra': 0x5,
    'or': 0x6,
    'and': 0x7,
    'addi': 0x0,
    'slti': 0x2,
    'sltiu': 0x3,
    'xori': 0x4,
    'ori': 0x6,
    'andi': 0x7,
    'slli': 0x1,
    'srli': 0x5,
    'srai': 0x5,
    'lb': 0x0,
    'lh': 0x1,
    'lw': 0x2,
    'lbu': 0x4,
    'lhu': 0x5,
    'sb': 0x0,
    'sh': 0x1,
    'sw': 0x2,
    'beq': 0x0,
    'bne': 0x1,
    'blt': 0x4,
    'bge': 0x5,
    'bltu': 0x6,
    'bgeu': 0x7,
    'jalr': 0x0,
    # Add more funct3 as needed
}

# Register mapping
registers = {
    'x0': 0, 'zero': 0,
    'x1': 1, 'ra': 1,
    'x2': 2, 'sp': 2,
    'x3': 3, 'gp': 3,
    'x4': 4, 'tp': 4,
    'x5': 5, 't0': 5,
    'x6': 6, 't1': 6,
    'x7': 7, 't2': 7,
    'x8': 8, 's0': 8, 'fp': 8,
    'x9': 9, 's1': 9,
    'x10': 10, 'a0': 10,
    'x11': 11, 'a1': 11,
    'x12': 12, 'a2': 12,
    'x13': 13, 'a3': 13,
    'x14': 14, 'a4': 14,
    'x15': 15, 'a5': 15,
    'x16': 16, 'a6': 16,
    'x17': 17, 'a7': 17,
    'x18': 18, 's2': 18,
    'x19': 19, 's3': 19,
    'x20': 20, 's4': 20,
    'x21': 21, 's5': 21,
    'x22': 22, 's6': 22,
    'x23': 23, 's7': 23,
    'x24': 24, 's8': 24,
    'x25': 25, 's9': 25,
    'x26': 26, 's10': 26,
    'x27': 27, 's11': 27,
    'x28': 28, 't3': 28,
    'x29': 29, 't4': 29,
    'x30': 30, 't5': 30,
    'x31': 31, 't6': 31,
}

def get_register(reg_string):
    reg_string = reg_string.strip(',')
    if reg_string in registers:
        return registers[reg_string]
    else:
        print(f"Error: Unknown register {reg_string}")
        sys.exit(1)
        
def parse_immediate(imm_str):
    # Check if the string starts with '0x' or '0X' indicating hexadecimal
    if imm_str.startswith('0x') or imm_str.startswith('0X'):
        return int(imm_str, 16)
    
    return int(imm_str)
        

def assemble_r_type(opcode, rd, funct3, rs1, rs2, funct7):
    instruction = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    bin_instr = format(instruction, '032b')
    print(bin_instr)
    return bin_instr

def assemble_i_type(opcode, rd, funct3, rs1, imm):
    # Ensure imm is masked to 12 bits
    imm &= 0xFFF
    instruction = (imm) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    bin_instr = format(instruction, '032b')
    print(bin_instr)
    return bin_instr


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
    #print(split_line)                        #for debug
    
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
        rd = get_register(split_line[1])
        r1 = get_register(split_line[2])
        r2 = get_register(split_line[3])
        func7 = op_funct7.get(mnemonic)
        func3 = op_funct3.get(mnemonic)
        machinecode = assemble_r_type(opCode, rd, func3, r1, r2, func7)
    
    elif opType == 'i_opType':
        #format is mnmemonic rd, rs1, imm_Value
        #also require funct3
        rd = get_register(split_line[1])
        r1 = get_register(split_line[2])
        imm = parse_immediate(split_line[3])
        func3 = op_funct3.get(mnemonic)
        machinecode = assemble_i_type(opCode, rd, func3, r1, imm)
asmFile.close()