from lookup_table import registers, op_type, op_code, op_funct7, op_funct3
import sys

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

