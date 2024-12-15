import numpy as np
import curses

with open("day-15/test-input.txt", "r") as file:
    input = file.read()

expand_lookup = {"#": "##", "O": "[]", ".": "..", "@": "@."}

warehouse_map, moves = [part.splitlines() for part in input.split("\n\n")]
warehouse_map = np.array(
    [
        [expanded_item for item in line for expanded_item in expand_lookup[item]]
        for line in warehouse_map
    ]
)

moves = "".join(moves)

map_indices = np.stack(np.indices(warehouse_map.shape), axis=-1)


def sanitise_1d(array, type: type):
    return tuple(type(item) for item in array)


def sanitise_2d(array, type: type):
    return [sanitise_1d(item, type) for item in array]


robot_location = sanitise_1d(map_indices[warehouse_map == "@"][0], int)


def get_new_location(location, move):
    return {
        ">": (location[0], location[1] + 1),
        "v": (location[0] + 1, location[1]),
        "<": (location[0], location[1] - 1),
        "^": (location[0] - 1, location[1]),
    }[move]


def basic_rayfind(start_location: tuple[int, int], move: str, max_length: int = None):
    row_index, column_index = start_location
    direction = {">": 1, "v": 1, "<": -1, "^": -1}[move]

    ray = [
        str(symbol)
        for symbol in {
            ">": warehouse_map[row_index, column_index::direction],
            "v": warehouse_map[row_index::direction, column_index],
            "<": warehouse_map[row_index, column_index::direction],
            "^": warehouse_map[row_index::direction, column_index],
        }[move]
    ]

    if max_length is None:
        max_length = len(ray)
    ray = ray[:max_length]

    compression_index = max_length - 1

    if "#" in ray:
        slice_index = ray.index("#")
        ray = ray[:slice_index]
        compression_index = slice_index - 1

    if "." in ray:
        compression_index = ray.index(".")

    slices = {
        ">": (row_index, slice(column_index, column_index + compression_index + 1)),
        "v": (slice(row_index, row_index + compression_index + 1), column_index),
        "<": (row_index, slice(column_index, column_index - compression_index - 1, -1)),
        "^": (slice(row_index, row_index - compression_index - 1, -1), column_index),
    }[move]

    return (
        ray,
        compression_index,
        slices,
        {True: [".", *ray[:compression_index]], False: None}["." in ray],
    )


def rayfind(start_location: tuple[int, int], move: str):
    branch_results = []
    changed_locations = []

    def branching_rayfind(ray, compression_index, slices, compressed_ray):
        new_branch_locations = []
        if move in ["v", "^"]:
            new_locations = [
                get_new_location(location, {"[": ">", "]": "<"}[symbol])
                for symbol, location in zip(
                    ray, sanitise_2d(map_indices[*slices][:compression_index], int)
                )
                if symbol in ["[", "]"]
            ]

            if any(location in changed_locations for location in new_locations):
                return True

            for location in new_locations:
                changed_locations.append(location)

            new_branch_locations = new_locations

        if compressed_ray is None:
            return False

        branch_results.append((ray, slices, compressed_ray))

        return all(
            [
                branching_rayfind(
                    *basic_rayfind(new_location, move, len(compressed_ray))
                )
                for new_location in new_branch_locations
            ]
        )

    can_move = branching_rayfind(*basic_rayfind(start_location, move))
    return branch_results if can_move else []


def print_map(terminal):
    try:
        for index, line in enumerate(warehouse_map):
            terminal.addstr(index + 1, 0, f"{''.join(line)}\n")
    except:
        for line in warehouse_map:
            print(f"{''.join(line)}")


def main_loop(terminal):
    global robot_location

    terminal.clear()
    terminal.addstr(f"Initial warehouse map:\n")
    print_map(terminal)
    terminal.getkey()

    for move_index, move in enumerate(moves):
        rays = rayfind(robot_location, move)
        for _, slices, compressed_ray in rays:
            if compressed_ray != None:
                warehouse_map[*slices] = compressed_ray

        if len(rays) > 0:
            robot_location = get_new_location(robot_location, move)

        terminal.clear()
        terminal.addstr(f"Warehouse map after move {move_index}({move}):\n")
        print_map(terminal)
        if move_index == len(moves) - 1:
            terminal.getkey()


curses.wrapper(main_loop)

# print(sum(
#     [
#         a + b
#         for a, b in zip(
#             (
#                 min(a, b)
#                 for a, b in zip(
#                     *(
#                         sanitise_1d(index_map[warehouse_map == "[", 0] * 100, int)
#                         for index_map in [map_indices, np.flipud(map_indices)]
#                     )
#                 )
#             ),
#             (
#                 min(a, b)
#                 for a, b in zip(
#                     *(
#                         sanitise_1d(index_map[warehouse_map == box_part, 1], int)
#                         for index_map, box_part in [
#                             (map_indices, "["),
#                             (np.fliplr(map_indices), "]"),
#                         ]
#                     )
#                 )
#             ),
#         )
#     ]
# ))
print(
    sum(sanitise_1d(np.sum(map_indices[warehouse_map == "["] * [100, 1], axis=-1), int))
)
