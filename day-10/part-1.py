import numpy as np

topological_map = np.genfromtxt("day-10/input.txt", dtype=int, delimiter=1)


def make_height_lookup(topological_map):
    height_coordinates = np.reshape(
        np.stack([topological_map, *np.indices(topological_map.shape)], axis=-1),
        [-1, 3],
    )
    return {
        height: sorted(
            [
                (row, col)
                for _, row, col in height_coordinates[
                    height_coordinates[:, 0] == height
                ]
            ]
        )
        for height in range(10)
    }


height_lookup = make_height_lookup(topological_map)


def magnitude(a, b):
    diff = np.subtract(a, b)
    return np.sqrt(diff.dot(diff))


def find_trail(coordinate):
    height = topological_map[*coordinate]
    if height == 9:
        return np.array(coordinate)[None, :]

    routes = [
        find_trail(next_step)
        for next_step in height_lookup[height + 1]
        if magnitude(next_step, coordinate) <= 1
    ]
    if len(routes) > 0:
        return np.unique(np.concatenate(routes, axis=0), axis=0)
    else:
        return np.empty([0, 2])


trail_scores = [find_trail(trailhead).shape[0] for trailhead in height_lookup[0]]

print(sum(trail_scores))
