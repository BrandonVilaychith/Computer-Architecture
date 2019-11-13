"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.power_status = True
        self.operations = {
            MUL: self.mul_operation,
            HLT: self.hlt_operation,
            PRN: self.prn_operation,
            LDI: self.ldi_operation
        }

    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # Read file from args
        # Loop through each line and separate from #
        # Convert the binary to a integer and add it to from address

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        f = open(file, "r")

        for line in f.readlines():
            split_line = line.split("#")[0]
            if split_line is "" or split_line is "\n":
                continue
            conversion = int(split_line, 2)
            self.ram[address] = conversion
            address += 1

        f.close()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            value = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = value
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def hlt_operation(self):
        self.power_status = False
        sys.exit()

    def ldi_operation(self, register, value):
        self.reg[register] = value
        self.pc += 3

    def prn_operation(self, register):
        value = self.reg[register]
        print(value)
        self.pc += 2

    def mul_operation(self, register_a, register_b):
        value = self.reg[register_a] * self.reg[register_b]
        self.reg[register_a] = value
        self.pc += 3

    def run(self):
        """Run the CPU."""
        while self.power_status is True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR is HLT:
                self.hlt_operation()
            elif IR is LDI:
                self.ldi_operation(operand_a, operand_b)
            elif IR is PRN:
                self.prn_operation(operand_a)
            elif IR is MUL:
                self.alu("MUL", operand_a, operand_b)



