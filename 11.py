def r1(s):
    return (True, 1) if s == 0 else (False, s)

def r2(s):
    if len(str(s)) % 2 != 0: return (False, s)
    mid = len(str(s)) // 2
    l, r = int(str(s)[:mid]), int(str(s)[mid:])
    return (True, (l, r))

def r3(s):
    return (True, s * 2024)

def r(s):
    b, s = r1(s)
    if b: return [s]
    b, s = r2(s)
    if b: return [*s]
    _, s = r3(s)
    return [s]

def iterate(stones):
    ss = {}
    for stone in stones.keys():
        s = r(stone)
        for x in s:
            if x not in ss:
                ss[x] = 0
            ss[x] += stones[stone]
    return ss

def solve(filename):
    stones = {}
    with open(filename, 'r') as file:
        for line in file:
            for stone in line.split(" "):
                stones[int(stone)] = 1
    
    # for _ in range(25):
    #     stones = iterate(stones)
    # print(sum(list(stones.values())))

    for _ in range(75):
        stones = iterate(stones)
    print(sum(list(stones.values())))


# solve("11.sample")
solve("11.input")
