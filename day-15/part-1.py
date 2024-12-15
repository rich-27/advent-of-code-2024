import numpy as np

with open("day-15/input.txt", "r") as file:
    input = file.read()

warehouse_map, moves = [part.splitlines() for part in input.split("\n\n")]
warehouse_map = np.array([list(line) for line in warehouse_map])
moves = "".join(moves)

map_indices = np.stack(np.indices(warehouse_map.shape), axis=-1)
robot_location = map_indices[warehouse_map == "@"][0]


def get_ray(map, location, move):
    row_index, column_index = location

    def get_slice(coord, ray: np.ndarray, direction=1):
        index_offset = ray.tolist().index("#")
        return slice(
            coord,
            (
                coord + direction * (index_offset + 1)
                if index_offset < len(ray) - 1
                else None
            ),
            direction,
        )

    match move:
        case ">":
            full_ray = map[row_index, column_index:]
            return (row_index, get_slice(column_index, full_ray))
        case "v":
            full_ray = map[row_index:, column_index]
            return (get_slice(row_index, full_ray), column_index)
        case "<":
            full_ray = map[row_index, column_index::-1]
            return (row_index, get_slice(column_index, full_ray, -1))
        case "^":
            full_ray = map[row_index::-1, column_index]
            return (get_slice(row_index, full_ray, -1), column_index)


def get_new_location(location, move):
    match move:
        case ">":
            return [location[0], location[1] + 1]
        case "v":
            return [location[0] + 1, location[1]]
        case "<":
            return [location[0], location[1] - 1]
        case "^":
            return [location[0] - 1, location[1]]


def get_move_result(ray: np.ndarray):
    index = ray.tolist().index(".")
    return [".", *ray[:index], *ray[index + 1 :]]


for move in moves:
    ray = warehouse_map[*get_ray(warehouse_map, robot_location, move)]
    if "." in ray:
        print(f"{move}: {''.join(ray)} => {''.join(get_move_result(ray))}")
        move_result = get_move_result(ray)
        warehouse_map[*get_ray(warehouse_map, robot_location, move)] = move_result
        robot_location = get_new_location(robot_location, move)
    else:
        print(f"{move}: {''.join(ray)} => None")

print(np.sum(map_indices[warehouse_map == 'O'] * [100, 1]))
