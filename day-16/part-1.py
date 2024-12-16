import numpy as np


def pathfind(starting_location):
    location_scores = {
        move: np.empty(reindeer_maze.shape, dtype=int) for move in move_lookup.keys()
    }

    paths = [
        (0, (starting_location[None, ...], [">"])),
        *(
            (1000, (starting_location[None, ...], [direction]))
            for direction in ["v", "^"]
        ),
        (2000, (starting_location[None, ...], ["<"])),
    ]
    complete_paths = {}
    min_score = None

    while len(paths) > 0:
        score, (locations, directions) = paths.pop(0)

        if min_score is not None and score > min_score:
            continue

        print(
            f"Looking {directions[-1]} from corner ({str(locations[-1][0]): >3}, {str(locations[-1][1]): >3}) (score = {score})..."
        )

        if len(complete_paths) > 0 and score < min_score:
            continue

        while True:
            next_location = np.add(locations[-1], move_lookup[directions[-1]])
            if np.all(locations == next_location, axis=1).any():
                break

            if (
                location_scores[directions[-1]][*next_location] > 0
                and location_scores[directions[-1]][*next_location] <= score
            ):
                break

            location_scores[directions[-1]][*next_location] = score

            locations = np.append(
                locations,
                next_location[None, ...],
                axis=0,
            )

            score += 1

            match reindeer_maze[*locations[-1]]:
                case "#":
                    break

                case "E":
                    if len(complete_paths) == 0:
                        min_score = score
                    else:
                        min(min_score, score)

                    if score not in complete_paths:
                        complete_paths[score] = [directions]
                    else:
                        complete_paths[score].append(directions)

                    break

            for move in turns_lookup[directions[-1]]:
                if reindeer_maze[*np.add(locations[-1], move_lookup[move])] != ".":
                    continue

                insert_index = len(
                    [
                        index
                        for index, (path_score, _) in enumerate(paths)
                        if path_score <= 1000 + score
                    ]
                )
                paths.insert(
                    insert_index,
                    (
                        score + 1000,
                        (locations, [*directions, move]),
                    ),
                )

            directions.append(directions[-1])

    return complete_paths


reindeer_maze = np.genfromtxt(
    "day-16/input.txt", dtype="U1", delimiter=1, comments=None
)
maze_indicies = np.indices(reindeer_maze.shape)

move_lookup = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
turns_lookup = {
    ">": ["v", "^"],
    "v": [">", "<"],
    "<": ["v", "^"],
    "^": [">", "<"],
}

paths = pathfind(maze_indicies[:, reindeer_maze == "S"][:, 0])
# for score, score_paths in paths.items():
#     for path in score_paths:
#         print(f"{score}: {path}")

print(min(paths.keys()))
