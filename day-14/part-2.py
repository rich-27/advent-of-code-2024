import curses

area_size = [101, 103]
with open("day-14/input.txt", "r") as file:
    input = file.readlines()

positions, velocities = zip(
    *(
        [[int(n) for n in part[2:].split(",")] for part in line.split(" ")]
        for line in input
    )
)


def print_on_grid(positions, terminal: curses.window = None):
    grid = [["." for _ in range(area_size[0])] for _ in range(area_size[1])]
    for x, y in positions:
        if grid[y][x] == ".":
            grid[y][x] = "1"
        else:
            grid[y][x] = str(int(grid[y][x]) + 1)
    for index, row in enumerate(grid):
        if terminal is None:
            print("".join(row))
        else:
            try:
                terminal.addstr(index + 1, 0, "".join(row))
            except:
                return
    if terminal is None:
        print()


def get_positions_at_time(time_elapsed):
    return [
        tuple(
            (position_component + velocity_component * time_elapsed)
            % area_size_component
            for position_component, velocity_component, area_size_component in zip(
                position, velocity, area_size
            )
        )
        for position, velocity in zip(positions, velocities)
    ]


def print_positions(terminal: curses.window):
    for elapsed_time in range(72, 10000, 103):
        terminal.clear()
        terminal.addstr(f"Position at {elapsed_time} seconds:\n")
        print_on_grid(get_positions_at_time(elapsed_time), terminal)
        terminal.getkey()


curses.wrapper(print_positions)

# Found 6870 through manual inspection:
# 1. Identify that every 103 seconds from 72 seconds onwards, there is lot of clumping
# 2. Step through trying to identify a pattern
# 3. Boom, christmas tree
