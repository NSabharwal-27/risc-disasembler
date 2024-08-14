# RISC-V Assembly Test File

# Test R-type instructions
add x1, x2, x3     # x1 = x2 + x3
sub x4, x5, x6     # x4 = x5 - x6
and x7, x8, x9     # x7 = x8 & x9
or  x10, x11, x12  # x10 = x11 | x12
xor x13, x14, x15  # x13 = x14 ^ x15
sll x16, x17, x18  # x16 = x17 << x18
slt x19, x20, x21  # x19 = (x20 < x21) ? 1 : 0
sra x22, x23, x24  # x22 = x23 >> x24 (arithmetic)
srl x25, x26, x27  # x25 = x26 >> x27 (logical)

# Test I-type instructions
addi x28, x29, 10  # x28 = x29 + 10
andi x30, x31, 0xFF # x30 = x31 & 0xFF
ori x1, x2, 0xF0F0  # x1 = x2 | 0xF0F0
xori x3, x4, 0x0F0F # x3 = x4 ^ 0x0F0F

# Test I-type load instructions
lw x5, 4(x6)       # x5 = Mem[x6 + 4]
lh x7, 2(x8)       # x7 = Mem[x8 + 2] (halfword)
lb x9, 1(x10)      # x9 = Mem[x10 + 1] (byte)
lbu x11, 0(x12)    # x11 = Mem[x12 + 0] (byte, unsigned)

# Test S-type instructions
sw x13, 8(x14)     # Mem[x14 + 8] = x13
sh x15, 6(x16)     # Mem[x16 + 6] = x15 (halfword)
sb x17, 4(x18)     # Mem[x18 + 4] = x17 (byte)

# Test B-type instructions
beq x19, x20, 12   # if (x19 == x20) PC += 12
bne x21, x22, -8   # if (x21 != x22) PC -= 8
blt x23, x24, 16   # if (x23 < x24) PC += 16
bge x25, x26, -4   # if (x25 >= x26) PC -= 4

# Test U-type instructions
lui x1, 0x12345    # x1 = 0x12345000
auipc x2, 0x6789A  # x2 = PC + 0x6789A000

# Test J-type instructions
jal x3, 1024       # x3 = PC + 4; PC += 1024
jalr x4, x5, 32    # x4 = PC + 4; PC = x5 + 32
