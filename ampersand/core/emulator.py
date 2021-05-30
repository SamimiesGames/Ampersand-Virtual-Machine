"""The Ampersand Emulator"""

# Registers

LDA = 0xF1  # Load A to C
LDB = 0xF2  # Load B to C
LDM = 0xF3  # Load Immidiate to C
STA = 0xF4  # Load C to A
STB = 0xF5  # Load C to B

# Memory and stack

STM = 0xF6  # Load B at C in memory
RTM = 0xF7  # Load C to B in memory

PSH = 0xa1  # Push C
POP = 0xa2  # Pop to C

# Calculations

ADD = 0x7  # Load A + B to C
SUB = 0x8  # Load A - B to C
DIV = 0x9  # Load A / B to C
MUL = 0xa  # Load A * B to C
EXP = 0xb  # Load A ** B to C

# Flow Control

NOP = 0x0  # Do Nothing
HLT = 0xFF  # Halt
JMP = 0xa3  # Jump to C
JZ = 0xa4  # Jump to C if zero
JL = 0xa5  # Jump to C if less than
JM = 0xa6  # Jump to C if more than


def create_memory():
    return {i: NOP for i in range(0xFFFF)}


class App:
    def __init__(self):
        self.memory = create_memory()
        self.stack = create_memory()

        self.pc = 0xFFFC
        self.sp = 0x0

        self.a = 0
        self.b = 0
        self.c = 0

        self.z = False
        self.o = False
        self.u = False

    def run(self):
        while self.pc <= 0xFFFF:
            optcode = self.bytelike(self.memory[self.pc])

            if optcode == LDA:
                self.c = self.a
            elif optcode == LDB:
                self.c = self.b
            elif optcode == STA:
                self.a = self.c
            elif optcode == STB:
                self.b = self.c
            elif optcode == LDM:
                self.pc += 1
                self.c = self.bytelike(self.memory[self.pc])
            elif optcode == STM:
                self.memory[self.c] = self.b
            elif optcode == RTM:
                self.c = self.bytelike(self.memory[self.b])
            elif optcode == PSH:
                self.stack[self.sp] = self.c
                self.sp += 1
            elif optcode == POP:
                self.c = self.stack[self.sp]
                self.sp -= 1
            elif optcode == ADD:
                self.c = self.bytelike(self.a + self.b)
                self.z, self.u, self.o = False, False, False

                self.z = self.c == 0
                self.u = self.c < 0
                self.o = self.c > 0
            elif optcode == SUB:
                self.c = self.bytelike(self.a - self.b)
                self.z, self.u, self.o = False, False, False

                self.z = self.c == 0
                self.u = self.c < 0
                self.o = self.c > 0
            elif optcode == DIV:
                self.c = self.bytelike(self.a / self.b)
            elif optcode == MUL:
                self.c = self.bytelike(self.a * self.b)
            elif optcode == EXP:
                self.c = self.bytelike(self.a ** self.b)
            elif optcode == JMP:
                self.pc = self.c - 1
            elif optcode == JZ:
                if self.z:
                    self.pc = self.c - 1
            elif optcode == JL:
                if self.u:
                    self.pc = self.c - 1
            elif optcode == JM:
                if self.o:
                    self.pc = self.c - 1
            elif optcode == HLT:
                break

            self.pc += 1

    @staticmethod
    def bytelike(value):
        if value > 0xFFFF:
            return 0xFFFF
        elif value < -0xFFFF:
            return -0xFFFF
        else:
            return value
