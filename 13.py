from z3 import *
from pprint import pprint

def parse_button(s) -> tuple[int, int]:
    return (
        int(s.split('X+')[1].split(',')[0]),
        int(s.split('Y+')[1])
    )

def parse_puzzle(s) -> tuple[int, int]:
    return (
        int(s.split('X=')[1].split(',')[0]),
        int(s.split('Y=')[1])
    )

def parse_puzzle2(s) -> tuple[int, int]:
    return (
        int(s.split('X=')[1].split(',')[0]) + 10000000000000,
        int(s.split('Y=')[1]) + 10000000000000
    )

def solve(filename):
    puzzles = []
    with open(filename, 'r') as file:
        groups = file.read().strip().split('\n\n')
        for group in groups:
            puzzles.append(group.split('\n'))

    total = 0
    for puzzle in puzzles:
        assert(len(puzzle) == 3)
        ax, ay = parse_button(puzzle[0])
        bx, by = parse_button(puzzle[1])
        x, y = parse_puzzle2(puzzle[2])

        opt = Optimize()
        n1 = Int('n1')
        n2 = Int('n2')

        opt.add(ax * n1 + bx * n2 == x)
        opt.add(ay * n1 + by * n2 == y)
        opt.add(n1 >= 0, n2 >= 0)

        # button 1 is a x3 more expensive than 2
        total_cost = (3 * n1) + n2
        opt.minimize(total_cost)

        if opt.check() == sat:
            model = opt.model()
            # print(puzzle, model)
            total += model.eval(total_cost).as_long()

    print(total)

# solve("13.sample")
solve("13.input")
