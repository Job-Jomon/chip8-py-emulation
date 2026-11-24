
# Create mychip8.py and write a Chip8 class with:

# memory: 4096 bytes, all zero to start (hint: bytearray(4096))
# v: 16 registers, all zero (a plain list works)
# pc: the program counter, starting at 0x200 (programs always load there)
# a load_rom(path) method that reads a ROM file and copies its bytes into memory starting at address 0x200 (hints: open(path, "rb") and f.read() to get the bytes, and slice assignment like memory[a:b] = data)

# Then make it prove it works. After loading the IBM logo ROM, print the first two bytes of the program in hex:

class Chip8:
    def __init__(self):
        self.memory = [0]*4096
        self.v = [0]*16
        self.pc = 0x200
        self.i = 0
        self.display = [[0] * 64 for _ in range(32)]

    def load_rom(self, path):
        with open(path, "rb") as f:
            data = f.read()
            self.memory[self.pc:(self.pc+len(data))] = data

    def fetch(self):
        a = self.memory[self.pc]
        b = self.memory[self.pc+1]
        c =(a << 8)
        c = (a << 8) | b
        self.pc += 2
        return c

    def decode(self, opcode):
        kind = (opcode & 0xF000) >> 12
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        n = (opcode & 0x000F) >> 0
        nn = (opcode & 0x0FF) >> 0
        nnn = (opcode & 0xFFF) >> 0
        return kind, x, y, n, nn, nnn

    def execute(self, opcode):
        kind, x, y, n, nn, nnn = self.decode(opcode)
        if opcode == 0x00E0:
            self.display = [[0] * 64 for _ in range(32)]
        elif kind == 0x1:
            self.pc = nnn
        elif kind == 0x6:
            self.v[x] = nn
        elif kind == 0x7:
            self.v[x] += nn
        elif kind == 0xA:
            self.i = nnn
        elif kind == 0xD:
            self.draw(x,y,n)
        else:
            print(hex(opcode))

    def draw(self, x, y, n):
        vx = self.v[x] % 64
        vy = self.v[y] % 32
        for row in range(n):
            byte = self.memory[self.i + row]
            for col in range(8):
                if byte & (0x80 >> col):
                    self.display[vy + row][vx + col] ^= 1








c = Chip8()
c.load_rom("2-ibm-logo.ch8")

for _ in range(200):
    c.execute(c.fetch())

print("START PRINT")
for row in c.display:
    print("".join("#" if p else " " for p in row))
print("END PRINT")

print(sum(sum(r) for r in c.display), c.v[0], c.v[1], hex(c.i))
