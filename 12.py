from pprint import pprint
from typing import List, Tuple
from itertools import groupby, product

def flood_fill(grid) -> List[List[Tuple[int, int]]]:
    visited = set([])
    regions = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) not in visited:
                region = []
                queue = [(i, j)]
                visited.add((i, j))
                while queue:
                    x, y = queue.pop(0)
                    region.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and (new_x, new_y) not in visited and grid[x][y] == grid[new_x][new_y]:
                            queue.append((new_x, new_y))
                            visited.add((new_x, new_y))
                regions.append(region)
    return regions

def area(region: List[Tuple[int, int]]) -> int:
    return len(region)

def perimeter(grid, region: List[Tuple[int, int]]) -> int:
    perimeter = 0
    value = grid[region[0][0]][region[0][1]]
    for x, y in region:
        default = 4
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and (new_x, new_y) in region:
                if grid[new_x][new_y] == value:
                    default -= 1
        perimeter += default
    return perimeter

def corners(grid, region: List[Tuple[int, int]]) -> int:
    corners = 0
    for x, y in region:
        for x_offset, y_offset in product([1, -1], repeat=2):
            row_neighbor = (x + x_offset, y)
            col_neighbor = (x, y + y_offset)
            diag_neighbor = (x + x_offset, y + y_offset)
            # check for exterior corners
            if row_neighbor not in region and col_neighbor not in region:
                corners += 1
            # check for interior corners
            if (
                row_neighbor in region and
                col_neighbor in region and
                diag_neighbor not in region
            ):
                corners += 1
    return corners

def solve(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append([c for c in line.strip()])
    regions = flood_fill(grid)

    price1, price2 = 0, 0
    for region in regions:
        a = area(region)
        p = perimeter(grid, region)
        c = corners(grid, region)
        price1 += a * p
        price2 += a * c

    print('part 1 :', price1)
    print('part 2 :', price2)


# solve("12.sample")
solve("12.input")
