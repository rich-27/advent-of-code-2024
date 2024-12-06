import numpy as np


def print_map(lab_map):
    for row in lab_map:
        print("".join(row))
    print()


def get_segment(lab_map, segment_indices):
    # print(segment_indices)
    return lab_map[*np.split(segment_indices, 2, axis=-1)][:, 0]


def get_next_segment(lab_map, guard_location, guard_direction):
    indices = np.stack(np.indices(lab_map.shape), axis=-1)
    segment_indices = np.squeeze(
        indices[
            *(
                *[
                    slice(
                        index,
                        index + 1 if move == 0 else None,
                        1 if move == 0 else move,
                    )
                    for index, move in zip(guard_location, guard_direction[0].move)
                ],
                slice(None),
            )
        ]
    )

    segment = get_segment(lab_map, segment_indices)

    are_obstacles = np.logical_or(segment == "#", segment == "O")
    if are_obstacles.sum() == 0:
        return (True, segment, segment_indices)

    segment_indices = segment_indices[
        : np.indices(segment.shape)[0][are_obstacles][0], :
    ]
    return (False, get_segment(lab_map, segment_indices), segment_indices)


def draw_path(map_array, path_indices, guard_direction):
    map_array[*np.split(path_indices, 2, axis=-1)] = guard_direction[0].symbol


def get_next_direction(guard_direction):
    return np.roll(guard_direction, -1, axis=0)


def find_path(lab_map, guard_location, guard_direction, has_obstacle=False):
    exits_map = False
    while not (exits_map):
        exits_map, path, path_indices = get_next_segment(
            lab_map, guard_location, guard_direction
        )

        # print(
        #     f"{lab_map.shape}, {guard_location}, {guard_direction[0].symbol}: {exits_map}, {path}, {path_indices.shape}"
        # )
        # print_map(lab_map)

        if not exits_map and path[-1] in guard_direction[:3].symbol:
            # if path[-1] == guard_direction[2].symbol or (
            #     path[-1] == guard_direction[3].symbol
            #     and lab_map[*np.add(path[-1], guard_direction[2].move)] in ["#", "O"]
            # ):
            # Path is looping
            return False

        draw_path(lab_map, path_indices, guard_direction)
        guard_direction = get_next_direction(guard_direction)
        guard_location = path_indices[-1]

        if path.size > 1 and not has_obstacle:
            is_starting_location = np.any(
                path_indices[:-1] != guard_starting_location, axis=1
            )
            loop_map_starting_locations = path_indices[:-1][is_starting_location]
            loop_map_count = is_starting_location.sum()
            loop_maps = np.repeat(np.copy(lab_map)[:, :, None], loop_map_count, axis=2)
            for map_index in range(loop_map_count):
                loop_maps[
                    *path_indices[1:][is_starting_location][map_index], map_index
                ] = "O"

            has_loop = np.logical_not(
                [
                    find_path(
                        np.squeeze(loop_map),
                        np.squeeze(start_location),
                        guard_direction,
                        True,
                    )
                    for loop_map, start_location in zip(
                        np.split(loop_maps, loop_map_count, axis=2),
                        np.split(
                            path_indices[:-1][is_starting_location],
                            loop_map_count,
                            axis=0,
                        ),
                    )
                ]
            )

            if has_loop.sum() > 0:
                global obstacle_locations
                obstacle_locations.append(path_indices[:-1][is_starting_location][has_loop])
            # if has_loop.sum() > 0:
            #     print(f'Found {has_loop.sum()} loops')
            #     global obstacle_maps
            #     obstacle_maps = np.append(obstacle_maps, loop_maps[:, :, has_loop], axis=2)

    return True


starting_lab_map = np.genfromtxt(
    "day-6/input.txt", dtype=str, delimiter=1, comments=None
)

guard_starting_location = np.array(
    [indices[0] for indices in np.where(starting_lab_map == "^")]
)
# Guard direction is first row of array
guard_direction = np.rec.fromrecords(
    [
        (direction, move)
        for direction, move in {
            "^": (-1, 0),
            ">": (0, 1),
            "v": (1, 0),
            "<": (0, -1),
        }.items()
    ],
    dtype=[("symbol", "U1"), ("move", tuple)],
)
# obstacle_maps = np.empty([*starting_lab_map.shape, 0])
obstacle_locations = []
find_path(starting_lab_map, guard_starting_location, guard_direction)

# print(np.any(obstacle_maps == "O", axis=2).sum())
print(np.unique(np.concatenate(obstacle_locations, axis=0), axis=0).shape[0])
print_map(starting_lab_map)
