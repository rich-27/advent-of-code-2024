import numpy as np


def pathfind(locations, directions):
    new_paths = []
    for new_direction, offset in move_lookup.items():
        new_location = np.add(locations[-1], offset)

        if np.all(locations == new_location, axis=1).any():
            continue

        symbol = reindeer_maze[*new_location]

        if symbol == "#":
            continue

        if symbol == "E":
            return [directions]

        new_paths.append(
            (
                np.append(locations, new_location[None, ...], axis=0),
                [*directions, new_direction],
            )
        )

    return [path for new_path in new_paths for path in pathfind(*new_path)]


def calculate_score(path):
    return len(path) + sum(
        [score_lookup[rotation] for rotation in zip(path[:-1], path[1:])]
    )


reindeer_maze = np.genfromtxt(
    "day-16/test-input.txt", dtype="U1", delimiter=1, comments=None
)
maze_indicies = np.indices(reindeer_maze.shape)

move_lookup = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
score_lookup = {
    (direction, new_direction): score
    for direction, score_lookup in {
        ">": {">": 0, "v": 1000, "<": 2000, "^": 1000},
        "v": {">": 1000, "v": 0, "<": 1000, "^": 2000},
        "<": {">": 2000, "v": 1000, "<": 0, "^": 1000},
        "^": {">": 1000, "v": 2000, "<": 1000, "^": 0},
    }.items()
    for new_direction, score in score_lookup.items()
}

start_location = maze_indicies[:, reindeer_maze == "S"][:, 0]
start_direction = ">"

paths = pathfind(start_location[None, :], [start_direction])
scores = [calculate_score(path) for path in paths]
for score, path in zip(scores, paths):
    print(f"{score}: {path}")

print(min(scores))
