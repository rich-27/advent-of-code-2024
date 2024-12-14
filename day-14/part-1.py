import math
from collections import Counter

area_size = [101, 103]
with open("day-14/input.txt", "r") as file:
    input = file.readlines()

# area_size = [11, 7]
# with open("day-14/test-input.txt", "r") as file:
#     input = file.readlines()

positions, velocities = zip(
    *(
        [[int(n) for n in part[2:].split(",")] for part in line.split(" ")]
        for line in input
    )
)


def print_on_grid(positions):
    grid = [["." for _ in range(area_size[0])] for _ in range(area_size[1])]
    for x, y in positions:
        if grid[y][x] == ".":
            grid[y][x] = "1"
        else:
            grid[y][x] = str(int(grid[y][x]) + 1)
    for row in grid:
        print("".join(row))
    print()


print_on_grid(positions)

final_positions = [
    tuple(
        (position_component + velocity_component * 100) % area_size_component
        for position_component, velocity_component, area_size_component in zip(
            position, velocity, area_size
        )
    )
    for position, velocity in zip(positions, velocities)
]

print_on_grid(final_positions)

quadrants = [
    tuple(
        0 if component == 0 else component // abs(component)
        for component in [
            position_component - (area_size_component // 2)
            for position_component, area_size_component in zip(position, area_size)
        ]
    )
    for position in final_positions
]

quadrant_counts = Counter(
    [
        quadrant
        for quadrant in quadrants
        if all(component != 0 for component in quadrant)
    ]
)

print(quadrant_counts)
print(math.prod(quadrant_counts.values()))
