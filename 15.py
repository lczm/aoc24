from pprint import pprint
from copy import deepcopy

def solve(filename):
    grid = []
    instructions = []
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        grid = [list(row) for row in lines[0].split('\n')]
        instructions = ''.join(lines[1].split('\n'))

    def resize(grid):
        new = []
        for row in grid:
            new_row = []
            for char in row:
                if char == '#':
                    new_row.append('#')
                    new_row.append('#')
                elif char == '@':
                    new_row.append('@')
                    new_row.append('.')
                elif char == '.':
                    new_row.append('.')
                    new_row.append('.')
                elif char == 'O':
                    new_row.append('[')
                    new_row.append(']')
            new.append(new_row)
        return new

    def vis(grid):
        return '\n'.join(''.join(row) for row in grid)

    def get_robot(grid):
        rx = ry = 0
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '@':
                    rx = row
                    ry = col
        return (rx, ry)
    
    def move_empty(grid, x, y, rx, ry):
        if grid[x][y] == '.':
            grid[x][y] = '@'
            grid[rx][ry] = '.'
            return True
        return False

    def glob_blocks(grid, x, y, dx, dy) -> list[tuple[int, int]]:
        # Essentially flood filling with a single dx, dy as a direction
        # Only used for globbing up or down the grid
        assert dy == 0
        assert dx == -1 or dx == 1
        if grid[x][y] == '.':
            return

        blocks = set([])
        # The first block that we see immediately
        queue= [(x, y)]

        # flood fill
        while queue:
            block = queue.pop()
            if block not in blocks:
                if grid[block[0]][block[1]] == '[':
                    queue.append((block[0], block[1]+1))
                elif grid[block[0]][block[1]] == ']':
                    queue.append((block[0], block[1]-1))

                blocks.add(block)
                bx, by = block
                bx += dx
                by += dy
                if grid[bx][by] == '[' or grid[bx][by] == ']':
                    queue.append((bx, by))

        return blocks

    def possible_to_move(grid, blocks, dx, dy) -> tuple[bool, list[tuple[int, int]]]:
        assert dy == 0
        assert dx == 1 or dx == -1

        # these coordinates will be where the newly placed cooridnates are
        new_blocks = [(block[0] + dx, block[1] + dy) for block in blocks]

        for block in new_blocks:
            if grid[block[0]][block[1]] != "." and block not in blocks:
                return (False, None)

        return (True, new_blocks)

    def move(grid, old_blocks, new_blocks, dx, dy):
        saved_grid = deepcopy(grid)

        for block in old_blocks:
            grid[block[0] + dx][block[1] + dy] = saved_grid[block[0]][block[1]]
        for block in old_blocks:
            if block not in new_blocks:
                grid[block[0]][block[1]] = '.'

    def part1(grid):
        rx, ry = get_robot(grid)
        for instruction in instructions:
            print(instruction)
            if instruction == '^': x, y = rx - 1, ry
            elif instruction == 'v': x, y = rx + 1, ry
            elif instruction == '<': x, y = rx, ry - 1
            elif instruction == '>': x, y = rx, ry + 1
            # hit the wall or moved to itself into an empty spot
            if grid[x][y] == '#': 
                continue
            if move_empty(grid, x, y, rx, ry):
                rx, ry = x, y
                continue
            # found a block, check if there is a empty spot
            dx, dy = x - rx, y - ry
            px, py = x, y
            while grid[px][py] == 'O':
                px += dx
                py += dy
            # check if its a wall, if it is, then nothing can be moved
            if grid[px][py] == '#':
                # print("Block, but no space")
                continue
            # there exists an empty space, move it
            if grid[px][py] == '.':
                grid[px][py] = 'O'
                grid[x][y] = '@'
                grid[rx][ry] = '.'
                rx, ry = x, y
                continue
        coordinates = []
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == 'O':
                    coordinates.append((100 * row) + col)
        print(vis(grid))
        print(sum(coordinates))

    def part2(grid):
        grid = resize(grid)
        rx, ry = get_robot(grid)
        print(vis(grid))

        for instruction in instructions:
            print(instruction)
            if instruction == '^': x, y = rx - 1, ry
            elif instruction == 'v': x, y = rx + 1, ry
            elif instruction == '<': x, y = rx, ry - 1
            elif instruction == '>': x, y = rx, ry + 1

            # hit the wall or moved to itself into an empty spot
            if grid[x][y] == '#': 
                # print(vis(grid))
                continue
            if move_empty(grid, x, y, rx, ry):
                rx, ry = x, y
                # print(vis(grid))
                continue
            # found a block, check if there is a empty spot
            dx, dy = x - rx, y - ry

            # if moving horizontally, then we can do the same as part1
            if dx == 0 and (dy == -1 or dy == 1):
                px, py = x, y
                while grid[px][py] == '[' or grid[px][py] == ']':
                    px += dx
                    py += dy
                # check if its a wall, if it is, then nothing can be moved
                if grid[px][py] == '#':
                    # print("Block, but no space")
                    continue
                # there exists an empty space, move it
                if grid[px][py] == '.':
                    # sanity check that the row is the same
                    assert x == px
                    # we need to swap every box character
                    for col in range(min(y, py), max(y, py)):
                        grid[x][col] = ']' if grid[x][col] == '[' else '['
                    # close off the box, depending on the position
                    grid[x][py] = '[' if dy == -1 else ']'
                    # move the robot
                    grid[x][y] = '@'
                    # set the old robot spot to be an empty space
                    grid[rx][ry] = '.'
                    rx, ry = x, y
                    # print(vis(grid))
                    continue
            # moving vertically, need to find the entire glob of blocks
            else:
                blocks = glob_blocks(grid, x, y, dx, dy)
                possible, new_blocks = possible_to_move(grid, blocks, dx, dy)
                if possible:
                    move(grid, blocks, new_blocks, dx, dy)
                    # move the robot up
                    grid[x][y] = '@'
                    grid[rx][ry] = '.'
                    rx, ry = x, y
                # print(vis(grid))
        
        coordinates = []
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '[':
                    coordinates.append((100 * row) + col)

        # print(vis(grid))
        print(sum(coordinates))
        

    part2(grid)
            
    


# solve("15.sample")
solve("15.input")
