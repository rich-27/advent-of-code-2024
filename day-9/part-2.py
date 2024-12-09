import numpy as np

dense_file_map = np.append(
    np.genfromtxt("day-9/input.txt", dtype=int, delimiter=1), [0]
).reshape([-1, 2])

file_map = np.array(
    [
        block
        for index, (file_size, free_size) in enumerate(dense_file_map)
        for block in [
            *(index for _ in range(file_size)),
            *(-1 for _ in range(free_size)),
        ]
    ]
)

free_spaces = {}
free_space_lookup = {n: [] for n in range(1, np.max(dense_file_map) + 1)}
head = 0
for free_id, (file_size, size) in enumerate(dense_file_map):
    head += file_size
    if size == 0:
        continue

    for n in range(1, size + 1):
        free_space_lookup[n].append(free_id)

    free_spaces[free_id] = (head, size)
    head += size

tail = file_map.size
for file_id in range(file_map[-1], 0, -1):
    tail -= np.sum(dense_file_map[file_id])

    size = dense_file_map[file_id, 0]

    if len(free_space_lookup[size]) == 0:
        continue

    free_id = free_space_lookup[size][0]
    head, free_size = free_spaces[free_id]

    if head > tail:
        continue

    new_size = free_size - size
    free_spaces[free_id] = (head + size, new_size)

    for n in range(free_size, new_size, -1):
        free_space_lookup[n].remove(free_id)

    file_map[head : head + size] = file_map[tail : tail + size]
    file_map[tail : tail + size] = -1

file_map[file_map == -1] = 0

print(np.sum(np.multiply(file_map, range(file_map.size)), dtype=np.int64))
