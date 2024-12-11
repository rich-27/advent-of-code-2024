import numpy as np
from itertools import islice

directions = ["^", ">", "v", "<"]
next_direction_lookup = dict(zip(directions, np.roll(directions, -1)))

obstacles = ["#", "O"]

bcolor_lookup = {
    "p": "\033[95m",
    "b": "\033[94m",
    "c": "\033[96m",
    "g": "\033[92m",
    "y": "\033[93m",
    "r": "\033[91m",
    "w": "\033[0m",
}

symbol_colour_lookup_base = {".": "c", "#": "r", "O": "y", "X": "p"}

symbol_colour_lookup = {
    **symbol_colour_lookup_base,
    **{item: "b" for item in directions},
}
check_path_symbol_colour_lookup = {
    **symbol_colour_lookup_base,
    **{item: "g" for item in directions},
}

lab_map = np.rec.fromrecords(
    [
        [(symbol_colour_lookup[item], item) for item in row]
        for row in np.genfromtxt(
            "day-6/input.txt", dtype=str, delimiter=1, comments=None
        )
    ],
    dtype=[("format", "U1"), ("symbol", "U1")],
)

guard_location = np.array([indices[0] for indices in np.where(lab_map.symbol == "^")])

indices = np.stack(np.indices(lab_map.shape[:2]), axis=-1)

paths_lookup = {}
checked_paths = []


def print_map(lab_map, with_obstacles=False):
    print(f"{bcolor_lookup['w']}+{''.join('-' for _ in range(lab_map.shape[1]))}+")

    map_to_print = np.copy(lab_map)

    if with_obstacles:
        for obstacle_location in obstacle_locations:
            map_to_print[*obstacle_location] = symbol_colour_lookup["O"]
    for row in map_to_print:
        print(
            f"{bcolor_lookup['w']}|{''.join([f'{bcolor_lookup[item.format]}{item.symbol}' for item in row])}{bcolor_lookup['w']}|"
        )

    print(f"{bcolor_lookup['w']}+{''.join('-' for _ in range(lab_map.shape[1]))}+")


def get_segment_indices(location, direction):
    match direction:
        case "^":
            return indices[location[0] :: -1, location[1]]
        case ">":
            return indices[location[0], location[1] :]
        case "v":
            return indices[location[0] :, location[1]]
        case "<":
            return indices[location[0], location[1] :: -1]


def next_segment(lab_map, location, direction):
    segment_indices = get_segment_indices(location, direction)

    segment = np.rec.fromarrays(
        [segment_indices, lab_map[*np.unstack(segment_indices, axis=-1)].symbol],
        dtype=[("location", "i", (2,)), ("symbol", "U1")],
    )

    exits_map = False
    try:
        segment = segment[: np.isin(segment.symbol, obstacles).tolist().index(True)]
    except ValueError:
        exits_map = True

    return exits_map, segment


def set_segment(lab_map, segment, colour_lookup):
    lab_map[*np.unstack(segment.location, axis=-1)] = (colour_lookup[segment[0].symbol], segment[0].symbol)


def rotate(segment):
    segment = segment.copy()
    segment.symbol = next_direction_lookup(segment.symbol)
    return segment


def check_path(lab_map, location, obstacle_check=False):
    global paths_lookup
    colour_lookup = (
        symbol_colour_lookup if not obstacle_check else check_path_symbol_colour_lookup
    )

    exits_map = False
    path = {}
    while exits_map == False:
        direction = lab_map[*location].symbol

        step = (*(int(n) for n in location), str(direction))

        if step in path:
            # Looping
            break

        if obstacle_check:
            try:
                exits_map, path_suffix = paths_lookup[step]
                path = {**path, **path_suffix}
                break
            except KeyError:
                pass

        exits_map, segment = next_segment(lab_map, location, direction)

        path[step] = segment

        if not obstacle_check:
            for check_index in range(segment[:-1].shape[0]):
                obstacle_location = segment[check_index + 1].location
                if np.all(obstacle_location == guard_location):
                    continue

                check_map = lab_map.copy()

                if check_index > 0:
                    set_segment(check_map, segment[:check_index + 1], colour_lookup)

                check_location = segment[check_index].location
                symbol = check_map[*check_location].symbol
                check_map[*check_location].format, check_map[*check_location].symbol = (
                    colour_lookup[symbol],
                    next_direction_lookup[symbol],
                )
                check_map[*obstacle_location].format, check_map[*obstacle_location].symbol = (colour_lookup["O"], "O")

                check_path_loops, checked_path = check_path(
                    check_map, check_location, True
                )
                if check_path_loops:
                    # Path loops
                    obstacle_locations.append(obstacle_location)

                checked_paths.append(checked_path)

                # print_map(check_map)
                # pass

        set_segment(lab_map, segment, colour_lookup)

        location = segment[-1].location
        lab_map[*location].format, lab_map[*location].symbol = (
            (colour_lookup["X"], "X")
            if exits_map
            else (colour_lookup[next_direction_lookup[direction]], next_direction_lookup[direction])
        )

    for index, step in enumerate(path.keys()):
        paths_lookup[step] = (exits_map, dict(islice(path.items(), index, None)))

    return (not exits_map, path)


obstacle_locations = []
check_path(lab_map, guard_location)

locations_visited = np.logical_not(np.isin(lab_map.symbol, [".", "#"])).sum()
print(locations_visited)

print(len(checked_paths))

lab_map[*np.unstack(np.stack(obstacle_locations, axis=0), axis=-1)] = (symbol_colour_lookup["O"], "O")

print((lab_map.symbol == "O").sum())

# print(np.unique(np.stack(obstacle_locations, axis=0), axis=0).shape[0])
print_map(lab_map)
