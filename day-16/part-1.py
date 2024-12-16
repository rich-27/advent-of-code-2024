import numpy as np


def pathfind(starting_location):
    starting_id = (tuple(starting_location.tolist()), ">")
    paths = {starting_id: {0: [(starting_location[None, ...], [">"])]}}
    path_scores = [(0, starting_id)]
    complete_paths = {}

    while len(path_scores) > 0:
        score, id = path_scores.pop(0)
        (locations, directions) = paths[id][min(paths[id].keys())][0]

        for new_direction, turn_score in turns_lookup[directions[-1]].items():
            next_location = np.add(locations[-1], move_lookup[new_direction])

            symbol = reindeer_maze[*next_location]
            if symbol == "#" or np.all(locations == next_location, axis=1).any():
                continue

            id = (tuple(next_location.tolist()), new_direction)
            new_score = score + turn_score + 1
            new_path = (
                np.append(
                    locations,
                    next_location[None, ...],
                    axis=0,
                ),
                [*directions, new_direction],
            )

            if symbol == "E":
                if new_score not in complete_paths:
                    complete_paths[new_score] = [new_path]
                else:
                    complete_paths[new_score].append(new_path)

                break

            if id not in paths:
                paths[id] = {new_score: [new_path]}
            else:
                path_score = min(paths[id].keys())

                if new_score > path_score:
                    continue

                if new_score not in paths[id]:
                    paths[id][new_score] = []

                paths[id][new_score].append(new_path)

                if new_score == path_score:
                    continue

                if new_score < path_score:
                    path_scores = [
                        (score, path_id)
                        for score, path_id in path_scores
                        if path_id != id
                    ]

            path_scores.append((new_score, id))
            path_scores.sort(key=lambda score_pair: score_pair[0])

    return min(complete_paths.keys())


reindeer_maze = np.genfromtxt(
    "day-16/input.txt", dtype="U1", delimiter=1, comments=None
)
maze_indicies = np.indices(reindeer_maze.shape)

move_lookup = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
turns_lookup = {
    ">": {">": 0, "v": 1000, "^": 1000, "<": 2000},
    "v": {"v": 0, ">": 1000, "<": 1000, "^": 2000},
    "<": {"<": 0, "v": 1000, "^": 1000, ">": 2000},
    "^": {"^": 0, ">": 1000, "<": 1000, "v": 2000},
}

score = pathfind(maze_indicies[:, reindeer_maze == "S"][:, 0])
print(score)
