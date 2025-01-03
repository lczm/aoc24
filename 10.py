from pprint import pprint
from itertools import chain

def get_surrounding(grid, point):
    x, y = point
    surrounding_points = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            surrounding_points.append((new_x, new_y))
    return surrounding_points

def traverse(grid, trail_head):
    row, col = trail_head
    trail_head_value = grid[row][col]
    if trail_head_value == 9:
        return (row, col)
    surrounding = [
        point for point in get_surrounding(grid, trail_head)
        if grid[point[0]][point[1]] == trail_head_value + 1
    ]
    if len(surrounding) == 0:
        return None

    trails = [traverse(grid, surrounding_point) for surrounding_point in surrounding]
    trails = list(filter(lambda x: x is not None, trails))
    return trails

def flatten(l):
    return list(chain(*[flatten(x) if isinstance(x, list) else [x] for x in l]))

def solve(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append([int(char) for char in line.strip()])

    trail_heads = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                trail_heads.append((row, col))

    scores1, scores2 = {}, {}
    for trail_head in trail_heads:
        trails = list(set(flatten(traverse(grid, trail_head))))
        trails2 = list(flatten(traverse(grid, trail_head)))
        scores1[trail_head] = len(trails)
        scores2[trail_head] = len(trails2)

    print(sum(scores1.values()))
    print(sum(scores2.values()))

solve("10.sample")
solve("10.input")
