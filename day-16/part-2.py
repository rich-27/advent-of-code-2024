import numpy as np


def pathfind(starting_location):
    starting_id = (tuple(starting_location.tolist()), ">")
    paths = {starting_id: {0: [(starting_location[None, ...], [">"])]}}
    path_scores = [(0, starting_id)]
    complete_path = None
    complete_path_score = 0

    while len(path_scores) > 0:
        score, id = path_scores.pop(0)
        (locations, directions) = paths[id][min(paths[id].keys())][0]

        # print(f"Processing {id}: {score}")
        results = {}
        corner_messages = []
        for new_direction, turn_score in turns_lookup[directions[-1]].items():
            next_location = np.add(locations[-1], move_lookup[new_direction])

            symbol = reindeer_maze[*next_location]
            if symbol == "#":
                results[new_direction] = "#"
                continue

            if np.all(locations == next_location, axis=1).any():
                results[new_direction] = "i"
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

            if id not in paths:
                paths[id] = {new_score: [new_path]}
            else:
                path_score = min(paths[id].keys())

                if new_score > path_score:
                    results[new_direction] = "r"
                    continue

                if new_score not in paths[id]:
                    paths[id][new_score] = []

                paths[id][new_score].append(new_path)

                if new_score == path_score:
                    results[new_direction] = "r"
                    continue

                if new_score < path_score:
                    path_scores = [
                        (score, path_id)
                        for score, path_id in path_scores
                        if path_id != id
                    ]

            if symbol == "E":
                if complete_path is None or new_score < complete_path_score:
                    complete_path_score, complete_path = (new_score, new_path)

                results[new_direction] = "E"
                break

            path_scores.append((new_score, id))
            path_scores.sort(key=lambda score_pair: score_pair[0])

            if new_direction != directions[-1]:
                corner_messages.append(
                    f"Looking {new_direction} from corner ({str(locations[-1][0]): >3}, {str(locations[-1][1]): >3}) (score = {score})..."
                )
            results[new_direction] = "s"

        # if 'E' not in results.values():
        #     print(f"  {results['^']}")
        #     print(f"{results['<']} @ {results['>']}")
        #     print(f"  {results['v']}")
        # else:
        #     print(results)
        # for message in corner_messages:
        #     print(message)

    
    min_score_at_location = {}
    for (location, _), paths_by_score in paths.items():
        min_score = min(paths_by_score.keys())

        if location in min_score_at_location:
            min_score = min(min_score_at_location[location], min_score)
        
        min_score_at_location[location] = min_score
    
    paths_at_location = {}
    for (location, _), paths_by_score in paths.items():
        if location not in paths_at_location:
            paths_at_location[location] = []
        
        min_score = min_score_at_location[location]
        if min_score in paths_by_score:
            for path in paths_by_score[min_score]:
                paths_at_location[location].append(path)
    
    
    all_locations = set()
    def unpack_path(location):
        while True:
            location_as_tuple = tuple(location.tolist())
            all_locations.add(location_as_tuple)
            
            location_paths = paths_at_location[location_as_tuple]
            if len(location_paths) == 0:
                return

            if len(location_paths) == 1:
                path_locations = location_paths[0][0]
                if len(path_locations) < 2:
                    return

                location = path_locations[-2]
                continue
            
            for path in location_paths:
                path_locations = path[0]
                unpack_path(path_locations[-2])
                return

    unpack_path(complete_path[0][-1])
    print(len(complete_path[0]))
    print(len(all_locations))
    pass


for _ in range(10):
    print()

reindeer_maze = np.genfromtxt(
    "day-16/test-input.txt", dtype="U1", delimiter=1, comments=None
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
