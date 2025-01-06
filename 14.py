import math
from dataclasses import dataclass
from pprint import pprint

bounds_x = 101 
bounds_y = 103

# bounds_x = 11
# bounds_y = 7

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def move(self) -> None:
        self.x = (self.x + self.vx) % bounds_x
        self.y = (self.y + self.vy) % bounds_y

def visualize(robots):
    grid = [
        ['.' for _ in range(bounds_x)]
          for _ in range(bounds_y)
    ]
    for robot in robots:
        grid[robot.y][robot.x] = '1'
    return '\n'.join(''.join(row) for row in grid)


def solve(filename):
    robots = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split("p=")[1].split(" ")[0].split(','))
            vx, vy = map(int, line.strip().split("v=")[1].split(" ")[0].split(','))
            robots.append(Robot(x, y, vx, vy))

    for i in range(50000):
        vis = visualize(robots)
        print(robots[0])
        print("Second : ", i)
        print(vis)
        [robot.move() for robot in robots]

    left_vertical, right_vertical = bounds_x // 2, math.ceil(bounds_x / 2)
    left_horizontal, right_horizontal = bounds_y // 2, math.ceil(bounds_y / 2)

    left_vertical -= 1
    left_horizontal -= 1

    q1 = q2 = q3 = q4 = 0
    for robot in robots:
        if 0 <= robot.x <= left_vertical and 0 <= robot.y <= left_horizontal:
            q1 += 1
        elif 0 <= robot.x <= left_vertical and right_horizontal <= robot.y <= bounds_y:
            q2 += 1
        elif right_vertical <= robot.x <=  bounds_x and 0 <= robot.y <= left_horizontal:
            q3 += 1
        elif right_vertical <= robot.x <=  bounds_x and right_horizontal <= robot.y <= bounds_y:
            q4 += 1
    
    print(q1, q2, q3, q4)
    print(q1 * q2 * q3 * q4)


# solve("14.sample")
solve("14.input")
