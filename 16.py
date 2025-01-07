from pprint import pprint
from heapq import heappush, heappop
from copy import deepcopy
from collections import defaultdict

def vis(grid):
    return '\n'.join(''.join(row) for row in grid)

def vis_path(grid, path, start, end):
    path_grid = deepcopy(grid)
    path_grid[start[0]][start[1]] = 'S'
    path_grid[end[0]][end[1]] = 'E'
    for x, y in path[1:-1]:
        path_grid[x][y] = '*'
    return '\n'.join(''.join(row) for row in path_grid)

# returns (x, y, direction, cost)
def get_neighbors(pos, grid) -> list[tuple[int, int, int, int]]:
    x, y, current_dir = pos
    # Directions: 
    # 0 = up,
    # 1 = right
    # 2 = down
    # 3 = left
    moves = [
        (-1, 0, 0),  # up
        (1, 0, 2),   # down
        (0, 1, 1),   # right
        (0, -1, 3)   # left
    ]
    
    neighbors = []
    for dx, dy, new_dir in moves:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < len(grid) and 
            0 <= new_y < len(grid[0]) and 
            grid[new_x][new_y] != '#'):
            # Cost is 1001 if turning, 1 if continuing straight
            cost = 1 if new_dir == current_dir else 1001
            neighbors.append((new_x, new_y, new_dir, cost))
    
    return neighbors

def dijkstra(grid, start, end) -> tuple[int, list[list[tuple[int, int]]]]:
    queue = []

    initial_dir = 1  # east
    for d in range(4):
        initial_cost = 1000 if d != initial_dir else 0
        heappush(queue, (initial_cost, (start[0], start[1], d)))
    
    visited = set()
    came_from = defaultdict(list)  # Allow multiple paths to reach each state
    min_end_cost = float('inf')
    end_states = []  # Track all states that reach the end with minimum cost
    
    while queue:
        cost, current = heappop(queue)
        x, y, _ = current
            
        # If at the end
        if (x, y) == end:
            # Check if this is the optimal cost
            if cost < min_end_cost:
                min_end_cost = cost
                end_states = [current]
            elif cost == min_end_cost:
                end_states.append(current)
            continue
            
        if current in visited:
            continue
            
        visited.add(current)
        
        for new_x, new_y, new_dir, move_cost in get_neighbors(current, grid):
            next_state = (new_x, new_y, new_dir)
            next_cost = cost + move_cost
            if next_state not in visited and next_cost <= min_end_cost:
                heappush(queue, (next_cost, next_state))
                came_from[next_state].append(current)
    
    # Reconstruct all paths with minimum cost
    def reconstruct_path(end_state):
        paths = [[end_state]]
        while paths[0][0] != (start[0], start[1], initial_dir):
            new_paths = []
            for path in paths:
                current = path[0]
                for prev in came_from[current]:
                    new_paths.append([prev] + path)
            paths = new_paths
        return [[(x, y) for x, y, _ in path] for path in paths]
    
    all_paths = []
    for end_state in end_states:
        all_paths.extend(reconstruct_path(end_state))
    
    return min_end_cost, all_paths

def calculate_path_cost(path: list[tuple[int, int]], initial_dir: int = 1) -> int:
    cost = 0
    current_dir = initial_dir
    direction_map = {
        (-1, 0): 0,  # up
        (1, 0): 2,   # down
        (0, 1): 1,   # right
        (0, -1): 3   # left
    }
    for i in range(len(path) - 1):
        dx, dy = path[i+1][0] - path[i][0], path[i+1][1] - path[i][1]
        new_dir = direction_map[(dx, dy)]
        if new_dir != current_dir:
            cost += 1000
        cost += 1
        current_dir = new_dir
    return cost

def solve(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    
    start = end = (0, 0)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start = (row, col)
            if grid[row][col] == 'E':
                end = (row, col)
    
    min_cost, paths = dijkstra(grid, start, end)
    print(f"min cost: {min_cost}")

    possible_seatings = set([])
    for path in paths:
        actual_cost = calculate_path_cost(path)
        if actual_cost != min_cost:
            continue
        # only add if it is the best path
        for point in path:
            possible_seatings.add(point)

    print(len(possible_seatings))

# solve("16.sample")
solve("16.input")

