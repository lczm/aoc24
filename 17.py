from math import pow

f = "17.sample"
f = "17.input"

with open(f, 'r') as file:
    lines = [line.strip() for line in file if line.strip()]

def parse(registers) -> list[int]:
    return [
        int(register.split(":")[1].strip())
        for register in registers
    ]

IP = 0
A, B, C = parse(lines[:3])
P = list(map(int, lines[-1].split(":")[1].strip().split(",")))
L = len(P)

class State:
    def __init__(self, A, B, C, IP=0):
        self.A = A
        self.B = B
        self.C = C
        self.IP = IP
        self.OUT = []

    def __str__(self):
        return (
            f"IP={self.IP}, "
            f"A={self.A}, "
            f"B={self.B}, "
            f"C={self.C}, "
            f"OUT={self.OUT}")


state = State(A, B, C, IP)

def op0(state: State, operand):
    state.A = int(state.A // pow(2, operand))
    state.IP += 2

def op1(state: State, operand):
    state.B = state.B ^ operand
    state.IP += 2

def op2(state: State, operand):
    state.B = operand % 8
    state.IP += 2

def op3(state: State, operand):
    if state.A != 0:
        state.IP = operand
    else:
        state.IP += 2

def op4(state: State, operand):
    state.B = state.B ^ state.C
    state.IP += 2

def op5(state: State, operand):
    state.OUT.append(operand % 8)
    state.IP += 2

def op6(state: State, operand):
    state.B = int(state.A // pow(2, operand))
    state.IP += 2

def op7(state: State, operand):
    state.C = int(state.A // pow(2, operand))
    state.IP += 2

def decode_operand(state, operand):
    if operand == 4: return state.A
    if operand == 5: return state.B
    if operand == 6: return state.C
    if operand >= 0 and operand <= 3:
        return operand

def compute(state):
    while True:
        opcode, operand = P[state.IP], P[state.IP+1]
        decoded_operand = decode_operand(state, operand)
        if opcode == 0: op0(state, decoded_operand)
        if opcode == 1: op1(state, decoded_operand)
        if opcode == 2: op2(state, decoded_operand)
        if opcode == 3: op3(state, decoded_operand)
        if opcode == 4: op4(state, decoded_operand)
        if opcode == 5: op5(state, decoded_operand)
        if opcode == 6: op6(state, decoded_operand)
        if opcode == 7: op7(state, decoded_operand)
        print(f"{state.IP:<3d}, {opcode}, {operand}, {state}")
        if state.IP > L - 1:
            break

def p1(x=0):
    if x != 0:
        state.A = x
    compute(state)
    print(','.join(map(str, state.OUT)))

def step(A):
    r = A & 7
    s = r ^ 3
    C = A >> s
    return (r ^ C) & 7

def p2():
    best = None
    def dfs(pos, nextA):
        nonlocal best
        if pos < 0:
            if best is None or nextA < best:
                best = nextA
            return
        required = P[pos]
        high = nextA
        for d in range(8):
            A_pos = (high << 3) | d
            if A_pos == 0:
                continue
            if step(A_pos) == required:
                dfs(pos - 1, A_pos)
    dfs(len(P) - 1, 0)
    print(best)

p2()
