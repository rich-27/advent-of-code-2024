import numpy as np

lab_map = np.genfromtxt("day-6/input.txt", dtype=str, delimiter=1, comments=None)

guard_location = np.array([indices[0] for indices in np.where(lab_map == "^")])

# Guard direction is first row of array
guard_direction = np.rec.fromrecords(
    [
        (direction, move)
        for direction, move in {
            "N": (-1, 0),
            "E": (0, 1),
            "S": (1, 0),
            "W": (0, -1),
        }.items()
    ],
    dtype=[("name", "U1"), ("move", tuple)],
)


def location_on_map(guard_location):
    return np.all(
        [index in range(size) for index, size in zip(guard_location, lab_map.shape)]
    )


indices = np.stack(np.indices(lab_map.shape), axis=-1)


def could_force_loop(lab_map, guard_location, guard_direction):
    match guard_direction[0].name:
        case "N":
            path = indices[guard_location[0], guard_location[1] :, :]
        case "E":
            path = indices[guard_location[0] :, guard_location[1], :]
        case "S":
            path = indices[guard_location[0], guard_location[1] :: -1, :]
        case "W":
            path = indices[guard_location[0] :: -1, guard_location[1], :]

    tiles = lab_map[*np.split(path, 2, axis=-1)][:, 0]
    if not np.any(tiles == "#"):
        return False

    path = path[: np.where(tiles == "#")[0][0], :]
    tiles = lab_map[*np.split(path, 2, axis=-1)][:, 0]
    if (
        tiles[-1] == guard_direction[2].name
        or tiles[-1] == guard_direction[3].name
        and lab_map[*np.add(path[-1], guard_direction[2].move)] == "#"
    ):
        return True

    lab_map[*np.split(path, 2, axis=-1)] = guard_direction[1].name
    return could_force_loop(lab_map, path[-1], np.roll(guard_direction, -1, axis=0))


obstacle_locations = []
is_on_map = True
while is_on_map:
    lab_map[*guard_location] = "*"
    next_location = np.add(guard_location, guard_direction[0].move)

    is_on_map = location_on_map(next_location)
    if not is_on_map:
        lab_map[*guard_location] = "X"
        # Reached border
        break

    if lab_map[*next_location] == "#":
        guard_direction = np.roll(guard_direction, -1, axis=0)
        continue

    if could_force_loop(np.copy(lab_map), guard_location, guard_direction):
        obstacle_locations.append(next_location)

    lab_map[*guard_location] = guard_direction[0].name
    guard_location = next_location

print(len(obstacle_locations))
