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


is_on_map = True
while is_on_map:
    next_location = np.add(guard_location, guard_direction[0].move)
    is_on_map = location_on_map(next_location)
    if not is_on_map:
        lab_map[*guard_location] = "X"
        # Reached border
        break

    match lab_map[*next_location]:
        case "#":
            guard_direction = np.roll(guard_direction, -1, axis=0)
        case "." | "X":
            lab_map[*guard_location] = "X"
            guard_location = next_location

locations_visited = (lab_map == "X").sum()
print(locations_visited)
